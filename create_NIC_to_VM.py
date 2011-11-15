#!/usr/bin/python
#
# Copyright (C) 2011
#
# Douglas Schilling Landgraf <dougsland@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import urllib2
import base64
import sys
from xml.etree import ElementTree

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

def getVMId(vm_name):

        URL      = "https://" + ADDR + ":" + API_PORT + "/api/vms"

        request = urllib2.Request(URL)

        base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
        request.add_header("Authorization", "Basic %s" % base64string)

        try:
                xmldata = urllib2.urlopen(request).read()
        except urllib2.URLError, e:
                print "Error: cannot connect to REST API: %s" % (e)
                print "\tTry to login using the same user/pass by the Admin Portal and check the error!"
                sys.exit(2)

        tree = ElementTree.XML(xmldata)
        list = tree.findall("vm")

        vm_id = None
        for item in list:
                if vm_name == item.find("name").text:
                        vm_id = item.attrib["id"]
                        print "vm id %s" % (vm_id)
                        break

        return vm_id

if __name__ == "__main__":

	if len(sys.argv) != 5:
		print "Usage: %s vm_name nic_name network_name nic_type (virtio/e1000/rtl8139/rtl8139_virtio)" %(sys.argv[0])
		print "Example: %s myVirtualMachine nic1 rhevm virtio" %(sys.argv[0])
		sys.exit(1)

	print "creating network to vm: %s" %(sys.argv[1])

	id_ret = getVMId(sys.argv[1])

	if id_ret == None:
		print "Cannot find virtual machine"
		sys.exit(1)

	xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<nic>
	  <interface>""" + sys.argv[4] + """</interface>
	  <name>""" + sys.argv[2] + """</name>
	  <network>
	    <name>""" + sys.argv[3] + """</name>
	  </network>
	</nic>
	"""

	#print xml_request

	# Setting URL
	URL      = "https://" + ADDR + ":" + API_PORT + "/api/vms/" + id_ret + "/nics"

	request = urllib2.Request(URL)
	print "Connecting to: " + URL

	base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)
	request.add_header('Content-Type', 'application/xml')

	try:
		ret = urllib2.urlopen(request, xml_request)
	except urllib2.URLError, e:
		print "%s" %(e)
		print "Are you trying to add an existing item?"
		sys.exit(-1)

	print "Done!"

# To see the response from the server 
#response = ret.read()
#print response
