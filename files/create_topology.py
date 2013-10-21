#!/usr/bin/env python

# Creates topology.dot file based on lldpctl output after all VMs come up.

import subprocess
import xml.etree.ElementTree as ET
import platform
from time import strftime

#get hostname of kvm host
kvmhostname = platform.node()

# get current date
current_date = strftime("%m/%d/%Y")

# read in lldpctl output
lldpxml = subprocess.check_output('lldpctl -f xml'.split())

#open dot file to write to
dotfile = open('/tmp/dotfile', 'w+')
dotfile.write('digraph G {\n')
dotfile.write('  graph [ hostidtype="hostname", ' + \
    'version="1:0",date="' + current_date + '"];\n')

#skamithiThinkPad:vnet1 -> vm1:eth1;
lldp_element = ET.fromstring(lldpxml)
for interface in lldp_element.iter('interface'):
  kvmhost_port = interface.attrib['name']
  remote_hostname = interface.findtext('chassis/name')
  remote_port = interface.findtext('port/descr')
  dotentry = kvmhostname + ':' + kvmhost_port + ' -> ' + \
      remote_hostname + ':' + remote_port + ';\n'
  dotfile.write('    ' + dotentry)

dotfile.write('}')
