#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
#
# simple-agent.py
# 
# Author:   Makoto Shimazu <makoto.shimaz@gmail.com>
# URL:      https://amiq11.tumblr.com               
# License:  2-Clause BSD License                    
# Created:  2016-03-27                              
#
#
# Copyright (c) 2016, Makoto Shimazu
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#



import sys
import dbus
import dbus.service
import dbus.mainloop.glib

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject


class Rejected(dbus.DBusException):
	_dbus_error_name = "org.bluez.Error.Rejected"

class Agent(dbus.service.Object):
    SPP_UUID = "00001101-0000-1000-8000-00805f9b34fb"

    @dbus.service.method("org.bluez.Agent1",
			 in_signature="", out_signature="")
    def Release(self):
	print "Release"
	mainloop.quit()

    @dbus.service.method("org.bluez.Agent1",
			 in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
	print "RequestPinCode (%s)" % (device)
        print "Default pin code is '0000'"
	return "0000"

    @dbus.service.method("org.bluez.Agent1",
                         in_signature="os", out_signature="")
    def DisplayPinCode(self, device, pincode):
        print "DisplayPinCode (%s, %s)" % (device, pincode)

    @dbus.service.method("org.bluez.Agent1",
			 in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
	print "RequestPasskey (%s)" % (device)
	passkey = raw_input("Enter passkey: ")
	return dbus.UInt32(passkey)

    @dbus.service.method("org.bluez.Agent1",
			 in_signature="ouq", out_signature="")
    def DisplayPasskey(self, device, passkey, entered):
	print "DisplayPasskey (%s, %d, %d)" % (device, passkey, entered)

    @dbus.service.method("org.bluez.Agent1",
			 in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, passkey):
	print "RequestConfirmation (%s, %d)" % (device, passkey)
	confirm = raw_input("Confirm passkey (yes/no): ")
	if (confirm == "yes"):
	    return
	raise Rejected("Passkey doesn't match")

    @dbus.service.method("org.bluez.Agent1",
                         in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        print "RequestAuthorization(%s)" % (device)
        return
# 	confirm = raw_input("Confirm authorization (yes/no): ")
# 	if (confirm == "yes"):
# 	    return
# 	raise Rejected("Rejected by user")

    @dbus.service.method("org.bluez.Agent1",
			 in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
	print "Authorize (%s, %s)" % (device, uuid)
        if (uuid == self.SPP_UUID):
            print "Authorized"
            return
	raise Rejected("Connection rejected; this agent accepts only SPP profile")

    @dbus.service.method("org.bluez.Agent1",
			 in_signature="", out_signature="")
    def Cancel(self):
	print "Cancel"

# def create_device_reply(device):
# 	print "New device (%s)" % (device)
# 	mainloop.quit()
# def create_device_error(error):
# 	print "Creating device failed: %s" % (error)
# 	mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	bus = dbus.SystemBus()
	manager = dbus.Interface(bus.get_object("org.bluez", "/org/bluez"),
				 "org.bluez.AgentManager1")
	path = "/com/pileproject/visebot/agent"
	agent = Agent(bus, path)
	mainloop = GObject.MainLoop()
        manager.RegisterAgent(path, "NoInputNoOutput")
	print "Agent registered"
        manager.RequestDefaultAgent(path)
	print "Default agent request successful"
	mainloop.run()
