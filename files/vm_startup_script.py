#!/usr/bin/env python

import subprocess
import xml.etree.ElementTree as ET
import re
import pdb
import os
import platform
from time import strftime

#
def getvirtioballon(vm_xml):
  memballon_xml = vm_xml.find('devices/memballoon/address')
  return '-device virtio-balloon-pci,id=balloon0,bus=pci.0,addr=' + \
      memballon_xml.attrib['slot'] + ' '

def getdiskstr(vm_xml):
  diskxml = vm_xml.find('devices/disk')
  diskaddress = diskxml.find('address')
  diskcontroller = diskaddress.attrib['controller']
  diskbus = diskaddress.attrib['bus']
  diskunit = diskaddress.attrib['unit']
  drivestr = '-drive format=qcow2,file=' + \
    diskxml.find('source').attrib['file'] + ',if=none,id=drive-ide' + \
    diskcontroller + '-' + diskbus + '-' + diskunit + ' '
  idestr = '-device ide-drive,bootindex=1,bus=ide.' + \
       diskbus + ',unit=' + diskunit + ',drive=drive-ide' + \
       diskcontroller + '-' + diskbus + '-' + diskunit + ' '
  return drivestr + idestr

def getchardev(vm_name):
  return '-chardev socket,id=charmonitor,path=/var/lib/libvirt/qemu/' + \
     vm_name + '.monitor,server,nowait '

def geteth(qemuxml, vm2vnet, vm_name):
  netstr = ''
  for hostnet, value in vm2vnet[vm_name].iteritems():
    # find interface tag that matches this mac address
    searchmac = ".//mac[@address='" + value['mac'] + "']/.."
    elem = qemuxml.find(searchmac)
    bridge = elem.find('source').attrib['bridge']
    bus = elem.find('address').attrib['bus']
    bus = str(int(bus,16))
    slot = elem.find('address').attrib['slot']
    if (bridge == 'basenet') or (bridge == 'mgmtnet'):
      # create tmp file with startup script
      filename =  '/tmp/' + vm_name + '_nic_startup.sh'
      startupscript = open(filename, 'w+')
      startupscript.write('#!/bin/bash \n')
      startupscript.write('ip link set ' + value['name'] + ' up promisc on \n')
      startupscript.write('/sbin/brctl addif ' + bridge + ' $1 \n')
      os.chmod(filename, 0755)
      netstr += '-netdev tap,script='+ filename + \
          ',id=host' + hostnet + ',vhost=on,ifname=' + value['name'] + ' '
      netstr += '-device virtio-net-pci,'
    else:
      listening_vm = re.search('^(vm\d{1})', bridge).group(0)
      port_number = '504' + re.search('\d+', bridge).group(0)
      netstr += '-netdev socket,id=host' + hostnet  + ','
      if (vm_name == 'vm4'):
        netstr += 'connect=127.0.0.1:' + port_number + ' '
      elif (listening_vm == vm_name) or (vm_name == 'vm1'):
        netstr += 'listen=127.0.0.1:' + port_number + ' '
      else:
        netstr += 'connect=127.0.0.1:' + port_number + ' '
      netstr += '-device rtl8139,'

    netstr += 'netdev=host' + hostnet + \
      ',id=' + hostnet + ',mac=' + value['mac'] + ',bus=pci.' + \
      bus + ',addr=' + slot + ' '
  return netstr

# Get mapping of [vmname][int] ->
# kvm_int_name
# Example: vm2net['vm1']['eth0'] => 'vnet0'

vm2vnet = {}
lldpxml = subprocess.check_output('lldpctl -f xml'.split())
lldp_element = ET.fromstring(lldpxml)

# develop a mapping that says something
# like this vm2net['vm3']['eth1'] = vnet1
for interface in lldp_element.iter('interface'):
  vm_name = interface.findtext('chassis/name')
  vm_net = interface.findtext('port/descr')
  vm_mac = interface.findtext('port/id')
  try:
    vm2vnet[vm_name]
  except KeyError:
    vm2vnet[vm_name] = {}

  vm2vnet[vm_name][vm_net] =  {}
  vm2vnet[vm_name][vm_net]['name'] = interface.attrib['name']
  vm2vnet[vm_name][vm_net]['mac'] =  vm_mac

default_values = [ "-machine", "pc-1.0", \
    "-enable-kvm", "-m","128", \
    "-smp","1,sockets=1,cores=1,threads=1", \
    "-no-shutdown", \
    "-rtc","base=utc", \
    "-mon","chardev=charmonitor,id=monitor,mode=control", \
    "-nodefconfig", \
    "-nodefaults", \
    "-vga","cirrus" ]

## create startup scripts for
scriptdir = '/tmp'
qemuvmdir = '/etc/libvirt/qemu'
vm_names = ['vm1', 'vm2', 'vm3','vm4']
for vm_name in vm_names:
  # open shell script to start vm
  filename = scriptdir + '/' + vm_name + '_startup.sh'
  hostscript = open(filename, 'w+')
  hostscript.write('#!/bin/bash\n')
  hostscript.write('#qemu start for ' + vm_name + '\n')

  # open xml file used by libvirt
  qemuxml = ET.parse(qemuvmdir + '/' + vm_name + '.xml').getroot()
  uuidstr = qemuxml.findtext('uuid')
  diskloc = qemuxml.find('devices/disk/source').attrib['file']

  startupstr = '/usr/bin/qemu-system-x86_64' + ' ' + ' '.join(default_values) + \
      ' -uuid ' + uuidstr + \
      ' ' + '-name ' + vm_name + ' -vnc 127.0.0.1:' + \
      re.search('vm(\d{1})', vm_name).group(1) + ' ' + \
    getdiskstr(qemuxml) + getchardev(vm_name) + \
    getvirtioballon(qemuxml) + geteth(qemuxml, vm2vnet, vm_name) + ' &\n' + \
    'exit \n'

  # write startup script to tmp directory
  hostscript.write(startupstr)
  os.chmod(filename, 0755)


