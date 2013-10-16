PTM Demo

Topology

PreRequisites.

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

* Configure SSH Key

Playbook expects to find a ```/tmp/id_rsa_ansible```
It copies this file into the first boot file for the created vms.

```
#ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/skamithi/.ssh/id_rsa):
/tmp/id_rsa_ansible
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /tmp/id_rsa_ansible.
Your public key has been saved in /tmp/id_rsa_ansible.pub.
The key fingerprint is:
2f:18:d4:1c:48:91:29:fd:3a:30:63:d5:b6:97:e8:d4
```

