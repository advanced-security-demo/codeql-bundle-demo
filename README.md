
## Requirements

* Ansible
* Vagrant
* Host Ports:
    * SSH: 2222
    * Apache: 8888

## Install

```
vagrant up
vagrant provision
```


## ProTip

Disable Host bastion catch all

```
# ~/.ssh/config
Host localhost
   ProxyCommand none
```


### Ansible not installed
```
The executable 'ansible-playbook' Vagrant is trying to run was not
found in the PATH variable. This is an error. Please verify
this software is installed and on the path.
```

