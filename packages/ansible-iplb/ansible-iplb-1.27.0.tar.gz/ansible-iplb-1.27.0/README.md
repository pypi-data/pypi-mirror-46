# Ansible IPLB Module

The aim of this repository is to provide an ansible module for handling ovh iplb

## Dev part

For CI, if you have docker, you can run `make ci`.
If you want something faster or don't want to run test using docker, you should use pyenv:
```
pyenv install $(cat ./python-version)
pyenv virtualenv $(cat ./python-version) ansible_iplb
pyenv activate ansible_iplb
pip install -r requirements/dev.txt
make test style
```

You can also run your module against real ovh api v6.
For that create a .env file with the following content:
```
SECRET_PATH_STORE=me/apiovh/token
LOAD_BALANCER=loadbalancer-xxxxxxxxxxxxxxxxxxxx
```
Or if you don't use pass:
```
LOAD_BALANCER=loadbalancer-c6f9b9aa43f6cc17bd51964011f48d76
OVH_APPLICATION_KEY=xxxxxxxxxxxx
OVH_APPLICATION_SECRET=xxxxxxxxxxxx
OVH_CONSUMER_KEY=xxxxxxxxxxxx
```

Those secrets will be used to populate the gomplate template `args.json`.
You can adapt it to test what you want.
Run your code with:
```
make run
```

# Installation part
```
pip install --extra-index-url https://pypi.ovh.net/simple ansible-iplb
```
