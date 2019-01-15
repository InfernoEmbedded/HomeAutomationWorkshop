#!/usr/bin/python

# Use DeviceMACs.txt to generate a configuration file for isc-dhcpd for the
# workshop at lca2019.

import re


from jinja2 import Template


ENTRY_RE = re.compile('^([0-9]+)\. +([0-9a-z:]+).*')

hosts = []
with open('DeviceMACs.txt') as f:
    for line in f.readlines():
        m = ENTRY_RE.match(line)
        if m:
            print('Host %s is %s' %(m.group(1), m.group(2)))
            hosts.append({'name': 'orangepi_%s' % m.group(1),
                          'mac': m.group(2),
                          'ip': int(m.group(1)) + 10})


with open('dhcpd.conf.tmpl') as f:
    t = Template(f.read())

with open('dhcpd.conf', 'w') as f:
    f.write(t.render(hosts=hosts))
