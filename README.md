This repository contains an example PHP application that is vulnerable to several different web application attacks.

## Requirements

* Ansible
* Vagrant
* Host Ports:
    * SSH: 2222
    * Apache: 8888


## SSH ProTip

Disable host bastion catch-all in `~/.ssh/config` by adding this line:

```
Host localhost
   ProxyCommand none
```

## Install

```
vagrant up
vagrant provision
```

### Ansible not installed
```
The executable 'ansible-playbook' Vagrant is trying to run was not
found in the PATH variable. This is an error. Please verify
this software is installed and on the path.
```
