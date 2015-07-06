## Description

This repository contains an example PHP application that is vulnerable to several different web application attacks.

## Requirements

* [Ansible][ansible]
* [Vagrant][vagrant]
* Host Ports:
    * SSH: 2222
    * Apache: 8888

## Install

```
vagrant up
vagrant provision
```

## Problems with install

### Vagrant SSH Issue
If SSH is set up to forward through a bastion on your machine, you'll need to add an exception in `~/.ssh/config` by adding this line:

```
Host localhost
   ProxyCommand none
```

### Ansible not installed
```
The executable 'ansible-playbook' Vagrant is trying to run was not
found in the PATH variable. This is an error. Please verify
this software is installed and on the path.
```

[ansible]: http://docs.ansible.com/intro_installation.html
[vagrant]: https://www.vagrantup.com/downloads.html
