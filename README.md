
## Requirements

* Ansible
* Vagrant
* Host Ports:
    * SSH: 2222
    * Apache: 8888


## ProTip

Disable Host bastion catch all

```
# ~/.ssh/config
Host localhost
   ProxyCommand none
```


## Install

```
vagrant up
vagrant provision
```

If you are setting up during the workshop and you use the box from the USB
stick, you will need to import the box first. On a Mac this might look like:
    `vagrant box add 'ubuntu/trusty64' /Volumes/USB\ DISK/ub64.box`

You can then run the rest of the install steps (should just need `vagrant up`)



### Ansible not installed
```
The executable 'ansible-playbook' Vagrant is trying to run was not
found in the PATH variable. This is an error. Please verify
this software is installed and on the path.
```

## Security Automation Tests

To run the first 2 security tests (demonstrated in the SQLi and XSS demos),
you can run the `security-demo.py` file. The `security-exercise.py` file has
the other two tests (from the exercise portion).
