## Description

This repository contains an example PHP application that is vulnerable to several different web application attacks.

## Requirements

* [Ansible][ansible]
* [Vagrant][vagrant]

## Install

```
vagrant up
vagrant provision
```

## WebApp Details

The web application can be accessed at [http://192.168.13.37/][webapp]. If you need to change anything in the app's VM, use `vagrant ssh`.

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
[webapp]: http://192.168.13.37/
