PTMD Demo
========

Ansible playbook to setup sandbox for me to test Cumulus Network's PTM Daemon.
Creates 4 VMs with 2 NICs. Attaches the 2 NICs to bridges configured on the KVM
Host. 

References
----------
[PTMD Presentation] [1]

[PTMD Source Code] [2]

[PTMD Demo done by Cumulus Network CEO] [3]. Not the main topic. Its part of a larger presentation regarding deploying massively scalable datacenter
Topology
--------
* Logical Topology

<pre>

|------|     |--------|
| VM1  |-----|  VM2   |
|------|     |--------|
   |            |
   |            |
   |            |
|------|     |--------|
| VM4  |-----|  VM3   |
|------|     |--------|


</pre>

PreRequisites.
--------------

* Requires Ubuntu 12.04 has KVM host

Runs only on Ubuntu 12.04 for now. Switching to ```virt-builder``` from
  ```vm-builder``` in next rework so I can test this on a debian/centos desktop.

* 4GB disk space in /var/ and 1 GB RAM freecen

Running it
----------

Host checking needs to be disabled because of all the changes the VMs undergo
during the creation process.

````
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook site.yml

````

What the Playbook does
-----------------------
* Installs KVM, libguest, Libvirt and Vm-builder on Ubuntu 12.04 Host
* Builds a fresh Ubuntu 12.04 image as a base VM
* Configures base VM with PTMD
* Clones base VM 3 times
* Configures clones with appropriate hostname 
* Configures eth1 and eth2 on all VMs
* Create startup scripts in /tmp directory, example /tmp/vm1_startup.sh

VMs must be started manually until I figure out how to get ansible to start a custom KVM call. 
```
# sudo /tmp/vm1_startup.sh
# sudo /tmp/vm2_startup.sh
# sudo /tmp/vm3.startup.sh
# sudo /tmp/vm4.startup.sh
```

Log into the hosts using hostnames from ```vm1``` to ```vm4```. Root account has public ssh key of the user you ran the ```ansible-playbook``` command from.

```
# ssh root@vm1
```

topology.dot file
-------------------------


```
digraph G {
  graph [ hostidtype="hostname", version="1:0",date="10/21/2013"];
    vm1:eth1 ->  vm2:eth1
    vm1:eth2 ->  vm4:eth2
    vm2:eth2 ->  vm3:eth2
    vm3:eth1 ->  vm4:eth1
}
```

ptmctl output
------------

Example ptmctl output from vm1

```
root@vm1:~# ptmctl
---------------------------------------------------------------------
Port   Status Expected Nbr         Observed Nbr         Last Updated
---------------------------------------------------------------------
eth1   pass   vm2:eth1             vm2:eth1              4m:25s   
eth2   pass   vm4:eth2             vm4:eth2              4m:25s  
```



Todo
----

~~Fix QEMU netdev issue so I get point to point connections between VMs. A must
for LLDP to flow between VMs~~

~~Add entry to /etc/hosts file for KVM server for each VM created~~

Write Ruby on Rails app first using graphviz to render the topology and than
after that leverage SVG, probably RaphaelJS and other libs. Web app will show
live changes in the topology has ```if-topo-pass``` and ```if-topo-fail``` get
activated.

[1]: http://indico.uknof.org.uk/getFile.py/access?contribId=8&resId=1&materialId=slides&confId=28
[2]: http://github.com/CumulusNetworks/ptm
[3]: http://www.youtube.com/watch?v=14qgJrbRYYU
