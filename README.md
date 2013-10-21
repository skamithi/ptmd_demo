PTM Demo
========

Ansible playbook to setup sandbox for me to test Cumulus Network's PTM Daemon.

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
  ```vm-builder``` in next rework so I can test this on a debian desktop.

* 4GB disk space in /var/ and 1 GB RAM free

Todo
----

Write Ruby on Rails app first using graphviz to render the topology and than
after that leverage SVG, probably RaphaelJS and other libs. Web app will show
live changes in the topology has ```if-topo-pass``` and ```if-topo-fail``` get
activated.


