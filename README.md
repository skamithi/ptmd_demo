PTM Demo

Topology

PreRequisites.

* Delete your ```$HOME/.ssh/known_hosts```. Clean this out so that there is no conflict
  with host keys in case you have used IP addresses that match the ones used in
this demo.

* Add authorized_keys to root directory on Ansible host
```
# Generate SSH key if you have already
> ssh-keygen

#copy the key to ~root/authorized_keys
> sudo cat .ssh/id_rsa.pub >> ~/root/.ssh/authorized_keys

```

* Disk and Memory Requirements

** 4GB disk free
** 1GB RAM free


