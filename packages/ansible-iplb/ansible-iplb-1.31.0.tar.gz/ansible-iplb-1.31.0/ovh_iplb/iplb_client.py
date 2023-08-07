import ovh
import ovh.exceptions
from ovh_iplb.utils import build_path, clean_unicode_of_dict, convert_key_to_camel_case
import time


def _real_payload_ok_with_wanted_payload(real_payload, wanted_payload):
    real_payload = clean_unicode_of_dict(real_payload)
    for k, v in clean_unicode_of_dict(wanted_payload).items():
        if v is not None and (k not in real_payload or real_payload[k] != v):
            return False
    return True


class Resource(object):

    def __init__(self,
                 parent,
                 resource_name,
                 id_field,
                 unique_field):
        self.parent = parent
        self.resource_name = resource_name
        self.id_field = id_field
        self.unique_field = unique_field
        self._id = None

    def client(self):
        return self.parent.client()

    def id(self):
        if self._id is not None:
            return self._id['id']

        self._id = {'id': self._find_id()}
        return self._id['id']

    def resource_path(self):
        return self.resource_name

    def base_path(self):
        return self.parent.path(self.resource_path())

    def path(self, *args):
        return build_path(self.base_path(), self.id(), *args)

    def get(self, *arg):
        return self.client().get(self.path(*arg))

    def delete_subresource(self, *arg):
        if len(arg) == 0:
            raise ValueError('You should at least specify one path')

        return self.client().delete(self.path(*arg))

    def subresource(self, subresource_name):
        return [self.get(subresource_name, id)
                for id in self.get(subresource_name)]

    def _find_id(self):
        unique_prop = self.body()[self.unique_field]
        resources = [r
                     for r in self.parent.subresource(self.resource_path())
                     if r[self.unique_field] == unique_prop]

        num_resources = len(resources)
        if num_resources == 0:
            return None
        elif num_resources > 1:
            raise ValueError('More than one %s found with %s:%s'
                             % (self.resource_name, self.unique_field, unique_prop))

        return resources[0][self.id_field]

    def read(self):
        return self.get()

    def exist(self):
        if not self.id():
            return False
        try:
            self.read()
            return True
        except ovh.ResourceNotFoundError:
            return False

    def create(self):
        id = self.client().post(self.base_path(), **self.body())[self.id_field]
        self._id = {'id': id}
        return id

    def update(self):
        if not self.id():
            raise ValueError('Could not update %s that does not exist' % (self.resource_name,))
        real_body = self.read()
        wanted_body = self.body()
        changement = not _real_payload_ok_with_wanted_payload(real_payload=real_body, wanted_payload=wanted_body)
        if changement:
            self.client().put(self.path(), **wanted_body)
        return changement

    def apply(self):
        if self.exist():
            return self.update()
        self.create()
        return True


class Server(Resource):

    def __init__(self, farm, server_def):
        Resource.__init__(self,
                          resource_name='server',
                          parent=farm,
                          id_field='serverId',
                          unique_field='address')
        self.server_def = server_def

    def body(self):
        return convert_key_to_camel_case({
            k: self.server_def[k]
            for k in ('address', 'backup', 'chain', 'display_name', 'port', 'probe',
                      'proxy_protocol_version', 'ssl', 'status', 'weight')
            if self.server_def.get(k) is not None
        })


class Farm(Resource):
    def __init__(self, iplb, farm_def):
        Resource.__init__(self,
                          resource_name='farm',
                          parent=iplb,
                          id_field='farmId',
                          unique_field='displayName',
                          )
        self.farm_def = farm_def

    def body(self):
        return convert_key_to_camel_case(
            dict(display_name=self.farm_def.get('name', None),
                 **{
                     k: self.farm_def[k]
                     for k in
                     ('balance', 'port', 'probe', 'zone', 'stickiness', 'vrack_network_id')
                     if self.farm_def.get(k) is not None
                 }))

    def id(self):
        return self.farm_def.get('id') or Resource.id(self)

    def resource_path(self):
        return build_path(self.farm_def['type'], 'farm')

    def server(self, server_def):
        return Server(self, server_def)

    def servers(self):
        return [self.server(server_def) for server_def in self.farm_def.get('servers', [])]

    def remove_orphan_server(self, servers=None):
        servers = servers or self.servers()
        id_to_remove = set(self.real_servers_id()) - {s.id() for s in servers}
        for id in id_to_remove:
            self.delete_subresource('server', id)

        return bool(id_to_remove)

    def real_servers_id(self):
        return self.get('server')

    def apply(self):
        change_on_iplb = Resource.apply(self)
        servers = self.servers()
        change_or_server_creation = any([s.apply() for s in servers])
        removed_orphan_server = self.remove_orphan_server(servers)

        return change_on_iplb or change_or_server_creation or removed_orphan_server


class IPLB(Resource):
    def __init__(self, iplb_def):
        self.iplb_def = iplb_def
        self._client = ovh.Client(endpoint=iplb_def['endpoint'],
                                  application_key=iplb_def['application_key'],
                                  application_secret=iplb_def['application_secret'],
                                  consumer_key=iplb_def['consumer_key'])

    def id(self):
        return self.iplb_def['iplb_id']

    def path(self, *args):
        return build_path('ipLoadbalancing', self.id(), *args)

    def farm(self, farm_def):
        return Farm(self, farm_def)

    def farms(self):
        return [self.farm(f) for f in self.iplb_def.get('farms', [])]

    def apply(self):
        self._sleep_until_no_task()
        change = any([f.apply() for f in self.farms()])
        is_refresh_needed = self.is_refresh_needed()
        if is_refresh_needed:
            self.refresh()

        return change or is_refresh_needed

    def client(self):
        return self._client

    def task_in_progress(self):
        return len(filter(lambda task: task['status'] != 'done', self.subresource('task'))) > 0

    def refresh(self):
        self.client().post(self.path('refresh'))
        self._sleep_until_no_task()

    def is_refresh_needed(self):
        return sum([zone.get('number', 0) for zone in self.get('pendingChanges')]) != 0

    def _sleep_until_no_task(self):
        currentTimeout = self.iplb_def['timeout']
        while self.task_in_progress():
            time.sleep(1)  # Delay for 1 sec
            currentTimeout -= 1
            if currentTimeout < 0:
                raise RuntimeError('timeout waiting for task to finish')
