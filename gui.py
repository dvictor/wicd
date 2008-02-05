#!/usr/bin/python

""" Wicd GUI module.

Module containg all the code (other than the tray icon) related to the 
Wicd user interface.

"""

#
#   Copyright (C) 2007 Adam Blackburn
#   Copyright (C) 2007 Dan O'Reilly
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License Version 2 as
#   published by the Free Software Foundation.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import signal
import time
import gettext
import locale
import gobject
import dbus
import dbus.service
import pango

import misc
import wpath

if __name__ == '__main__':
    wpath.chdir(__file__)
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk, gtk.glade
except:
    print 'Missing GTK and gtk.glade.  Aborting.'
    sys.exit(1)

if getattr(dbus, 'version', (0,0,0)) >= (0,41,0):
    import dbus.glib

# Declare the connections to the daemon, so that they may be accessed
# in any class.
bus = dbus.SystemBus()
try:
    print 'Attempting to connect daemon to GUI...'
    proxy_obj = bus.get_object('org.wicd.daemon', '/org/wicd/daemon')
    print 'Success'
except:
    print 'Daemon not running, trying to start it automatically.'
    misc.PromptToStartDaemon()
    time.sleep(1)
    try:
        proxy_obj = bus.get_object('org.wicd.daemon', '/org/wicd/daemon')
        print 'Daemon started succesfully'
    except:
        print 'Daemon still not running, aborting.'
        sys.exit(1)

daemon = dbus.Interface(proxy_obj, 'org.wicd.daemon')
wireless = dbus.Interface(proxy_obj, 'org.wicd.daemon.wireless')
wired = dbus.Interface(proxy_obj, 'org.wicd.daemon.wired')
vpn_session = dbus.Interface(proxy_obj, 'org.wicd.daemon.vpn')
config = dbus.Interface(proxy_obj, 'org.wicd.daemon.config')

_ = misc.get_gettext()

# Keep all the language strings in a dictionary
# by the english words.
# I'm not sure this is the best way to do it
# but it works and makes it easy for me :)
##########
# translations are done at
# http://wicd.net/translator
# please translate if you can!
##########
language = {}
language['connect'] = _("Connect")
language['ip'] = _("IP")
language['netmask'] = _("Netmask")
language['gateway'] = _('Gateway')
language['dns'] = _('DNS')
language['use_static_ip'] = _('Use Static IPs')
language['use_static_dns'] = _('Use Static DNS')
language['use_encryption'] = _('Use Encryption')
language['advanced_settings'] = _('Advanced Settings')
language['wired_network'] = _('Wired Network')
language['wired_network_instructions'] = _('To connect to a wired network, you'
' must create a network profile. To create a network profile, type a name that'
' describes this network, and press Add.')
language['automatic_connect'] = _('Automatically connect to this network')
language['secured'] = _('Secured')
language['unsecured'] = _('Unsecured')
language['channel'] = _('Channel')
language['preferences'] = _('Preferences')
language['wpa_supplicant_driver'] = _('WPA Supplicant Driver')
language['wireless_interface'] = _('Wireless Interface')
language['wired_interface'] = _('Wired Interface')
language['hidden_network'] = _('Hidden Network')
language['hidden_network_essid'] = _('Hidden Network ESSID')
language['connected_to_wireless'] = _('Connected to $A at $B (IP: $C)')
language['connected_to_wired'] = _('Connected to wired network (IP: $A)')
language['not_connected'] = _('Not connected')
language['no_wireless_networks_found'] = _('No wireless networks found.')
language['killswitch_enabled'] = _('Wireless Kill Switch Enabled')
language['key'] = _('Key')
language['username'] = _('Username')
language['password'] = _('Password')
language['anonymous_identity'] = _('Anonymous Identity')
language['identity'] = _('Identity')
language['authentication'] = _('Authentication')
language['path_to_pac_file'] = _('Path to PAC File')
language['select_a_network'] = _('Choose from the networks below:')
language['connecting'] = _('Connecting...')
language['wired_always_on'] = _('Always show wired interface')
language['auto_reconnect'] = _('Automatically reconnect on connection loss')
language['create_adhoc_network'] = _('Create an Ad-Hoc Network')
language['essid'] = _('ESSID')
language['use_wep_encryption'] = _('Use Encryption (WEP only)')
language['before_script'] = _('Run script before connect')
language['after_script'] = _('Run script after connect')
language['disconnect_script'] = _('Run disconnect script')
language['script_settings'] = _('Scripts')
language['use_ics'] = _('Activate Internet Connection Sharing')
language['madwifi_for_adhoc'] = _('Check if using madwifi/atheros drivers')
language['default_wired'] = _('Use as default profile (overwrites any previous default)')
language['use_debug_mode'] = _('Enable debug mode')
language['use_global_dns'] = _('Use global DNS servers')
language['use_default_profile'] = _('Use default profile on wired autoconnect')
language['show_wired_list'] = _('Prompt for profile on wired autoconnect')
language['use_last_used_profile'] =_ ('Use last used profile on wired autoconnect')
language['choose_wired_profile'] = _('Select or create a wired profile to connect with')
language['wired_network_found'] = _('Wired connection detected')
language['stop_showing_chooser'] = _('Stop Showing Autoconnect pop-up temporarily')
language['display_type_dialog'] = _('Use dBm to measure signal strength')
language['scripts'] = _('Scripts')
language['invalid_address'] = _('Invalid address in $A entry.')

language['0'] = _('0')
language['1'] = _('1')
language['2'] = _('2')
language['3'] = _('3')
language['4'] = _('4')
language['5'] = _('5')
language['6'] = _('6')
language['7'] = _('7')
language['8'] = _('8')
language['9'] = _('9')

language['interface_down'] = _('Putting interface down...')
language['resetting_ip_address'] = _('Resetting IP address...')
language['interface_up'] = _('Putting interface up...')
language['setting_encryption_info'] = _('Setting encryption info')
language['removing_old_connection'] = _('Removing old connection...')
language['generating_psk'] = _('Generating PSK...')
language['generating_wpa_config'] = _('Generating WPA configuration file...')
language['flushing_routing_table'] = _('Flushing the routing table...')
language['configuring_interface'] = _('Configuring wireless interface...')
language['validating_authentication'] = _('Validating authentication...')
language['setting_broadcast_address'] = _('Setting broadcast address...')
language['setting_static_dns'] = _('Setting static DNS servers...')
language['setting_static_ip'] = _('Setting static IP addresses...')
language['running_dhcp'] = _('Obtaining IP address...')
language['no_dhcp_offers'] = _('Connection Failed: No DHCP offers received.  \
                                Couldn\'t get an IP Address.')
language['dhcp_failed'] = _('Connection Failed: Unable to Get IP Address')
language['aborted'] = _('Connection cancelled')
language['bad_pass'] = _('Connection Failed: Bad password')
language['done'] = _('Done connecting...')

########################################
##### GTK EXTENSION CLASSES
########################################

class LinkButton(gtk.EventBox):
    label = None
    def __init__(self, txt):
        gtk.EventBox.__init__(self)
        self.connect("realize", self.__setHandCursor) #set the hand cursor when the box is initalized
        label = gtk.Label()
        label.set_markup("[ <span color=\"blue\">" + txt + "</span> ]")
        label.set_alignment(0,.5)
        label.show()
        self.add(label)
        self.show_all()

    def __setHandCursor(self,widget):
        # We need this to set the cursor to a hand for the link labels.
        # I'm not entirely sure what it does :P
        hand = gtk.gdk.Cursor(gtk.gdk.HAND1)
        widget.window.set_cursor(hand)

class SmallLabel(gtk.Label):
    def __init__(self,text=''):
        gtk.Label.__init__(self,text)
        self.set_size_request(50,-1)

class LabelEntry(gtk.HBox):
    '''a label on the left with a textbox on the right'''
    def __init__(self,text):
        gtk.HBox.__init__(self)
        self.entry = gtk.Entry()
        self.entry.set_size_request(200,-1)
        self.label = SmallLabel()
        self.label.set_text(text)
        self.label.set_size_request(170,-1)
        self.pack_start(self.label,fill=False,expand=False)
        self.pack_start(self.entry,fill=False,expand=False)
        self.label.show()
        self.entry.show()
        self.entry.connect('focus-out-event',self.hide_characters)
        self.entry.connect('focus-in-event',self.show_characters)
        self.auto_hide_text = False
        self.show()

    def set_text(self, text):
        # For compatibility...
        self.entry.set_text(text)

    def get_text(self):
        return self.entry.get_text()

    def set_auto_hidden(self, value):
        self.entry.set_visibility(False)
        self.auto_hide_text = value

    def show_characters(self, widget=None, event=None):
        # When the box has focus, show the characters
        if self.auto_hide_text and widget:
            self.entry.set_visibility(True)

    def set_sensitive(self, value):
        self.entry.set_sensitive(value)
        self.label.set_sensitive(value)

    def hide_characters(self, widget=None, event=None):
        # When the box looses focus, hide them
        if self.auto_hide_text and widget:
            self.entry.set_visibility(False)

class GreyLabel(gtk.Label):
    def __init__(self):
        gtk.Label.__init__(self)
    def set_label(self,text):
        self.set_markup("<span color=\"#666666\"><i>" + text + "</i></span>")
        self.set_alignment(0,0)

########################################
##### OTHER RANDOM FUNCTIONS
########################################

def noneToString(text):
    """Converts a blank string to "None". """
    if text == "":
        return "None"
    else:
        return str(text)

def noneToBlankString(text):
    """ Converts NoneType or "None" to a blank string. """
    if text == None or text == "None" or text == "":
        return ""
    else:
        return str(text)

def stringToNone(text):
    '''performs opposite function of noneToString'''
    if text == "" or text == "None" or text == None:
        return None
    else:
        return str(text)

def stringToBoolean(text):
    '''Turns a "True" to True or a "False" to False otherwise returns the text'''
    if text == "True":
        return True
    if text == "False":
        return False
    return text

def checkboxTextboxToggle(checkbox,textboxes):
    # Really bad practice, but checkbox == self
    for textbox in textboxes:
            textbox.set_sensitive(checkbox.get_active())

########################################
##### NETWORK LIST CLASSES
########################################


class PrettyNetworkEntry(gtk.HBox):
    '''Adds an image and a connect button to a NetworkEntry'''
    def __init__(self, expander):
        gtk.HBox.__init__(self)
        # Add the stuff to the hbox (self)
        self.expander = expander
        self.expander.show()
        self.expander.higherLevel = self  # Do this so that the expander can access the stuff inside me
        self.tempVBox = gtk.VBox(False, 1)
        self.tempVBox.show()
        self.connectButton = gtk.Button(stock=gtk.STOCK_CONNECT)
        connect_hbox = gtk.HBox(False, 2)
        connect_hbox.pack_start(self.connectButton, False, False)
        #connect_hbox.pack_start(self.expander.scriptButton, False, False)
        #connect_hbox.pack_start(self.expander.advancedButton, False, False)
        connect_hbox.show()
        self.tempVBox.pack_start(self.expander, fill=False, expand=False)
        self.tempVBox.pack_start(connect_hbox, fill=False, expand=False)
        self.pack_end(self.tempVBox)
        #self.expander.scriptButton.show()
        #self.expander.advancedButton.show()
        

class PrettyWiredNetworkEntry(PrettyNetworkEntry):
    def __init__(self):
        PrettyNetworkEntry.__init__(self, WiredNetworkEntry())
        # Center the picture and pad it a bit
        self.image = gtk.Image()
        self.image.set_alignment(.5, 0)
        self.image.set_size_request(60, -1)
        self.image.set_from_icon_name("network-wired", 6)
        self.image.show()
        self.pack_start(self.image, fill=False, expand=False)
        self.show()
        self.expander.checkEnable()
        self.expander.show()
        self.connectButton.show()


class PrettyWirelessNetworkEntry(PrettyNetworkEntry):
    def __init__(self,networkID):
        PrettyNetworkEntry.__init__(self, WirelessNetworkEntry(networkID))
        self.image = gtk.Image()
        self.image.set_padding(0, 0)
        self.image.set_alignment(.5 ,0)
        self.image.set_size_request(60, -1)
        self.image.set_from_icon_name("network-wired",6)
        self.pack_start(self.image, fill=False, expand=False)
        self.setSignalStrength(wireless.GetWirelessProperty(networkID, 'quality'),
                               wireless.GetWirelessProperty(networkID, 'strength'))
        self.setMACAddress(wireless.GetWirelessProperty(networkID, 'bssid'))
        self.setMode(wireless.GetWirelessProperty(networkID, 'mode'))
        self.setChannel(wireless.GetWirelessProperty(networkID, 'channel'))
        self.setEncryption(wireless.GetWirelessProperty(networkID, 'encryption'),
                           wireless.GetWirelessProperty(networkID, 'encryption_method'))
        self.expander.set_use_markup(True)
        self.expander.set_label(self.expander.essid + "   " + 
                                self.expander.lblEncryption.get_label() + "   "
                                + self.expander.lblStrength.get_label())
        # Show everything
        self.show_all()

    def setSignalStrength(self, strength, dbm_strength):
        if strength is not None:
            strength = int(strength)
        else:
            strength = -1
        if dbm_strength is not None:
            dbm_strength = int(dbm_strength)
        else:
            dbm_strength = -1
        display_type = daemon.GetSignalDisplayType()
        if daemon.GetWPADriver() == 'ralink legacy' or display_type == 1:
            # Use the -xx dBm signal strength to display a signal icon
            # I'm not sure how accurately the dBm strength is being
            # "converted" to strength bars, so suggestions from people
            # for a better way would be welcome.
            if dbm_strength >= -60:
                signal_img = 'signal-100.png'
            elif dbm_strength >= -70:
                signal_img = 'signal-75.png'
            elif dbm_strength >= -80:
                signal_img = 'signal-50.png'
            else:
                signal_img = 'signal-25.png'
        else:
            # Uses normal link quality, should be fine in most cases
            if strength > 75:
                signal_img = 'signal-100.png'
            elif strength > 50:
                signal_img = 'signal-75.png'
            elif strength > 25:
                signal_img = 'signal-50.png'
            else:
                signal_img = 'signal-25.png'
        self.image.set_from_file(wpath.images + signal_img)
        self.expander.setSignalStrength(strength, dbm_strength)

    def setMACAddress(self, address):
        self.expander.setMACAddress(address)

    def setEncryption(self, on, ttype):
        self.expander.setEncryption(on, ttype)

    def setChannel(self, channel):
        self.expander.setChannel(channel)

    def setMode(self, mode):
        self.expander.setMode(mode)


class NetworkEntry(gtk.Expander):
    '''The basis for the entries in the network list'''
    def __init__(self):
        # Make stuff exist, this is pretty long and boring.
        gtk.Expander.__init__(self)
        self.txtIP = LabelEntry(language['ip'])
        self.txtIP.entry.connect('focus-out-event', self.setDefaults)
        self.txtNetmask = LabelEntry(language['netmask'])
        self.txtGateway = LabelEntry(language['gateway'])
        self.txtDNS1 = LabelEntry(language['dns'] + ' ' + language['1'])
        self.txtDNS2 = LabelEntry(language['dns'] + ' ' + language['2'])
        self.txtDNS3 = LabelEntry(language['dns'] + ' ' + language['3'])
        self.vboxTop = gtk.VBox(False, 0)
        
        self.advancedButton = gtk.Button()
        advanced_image = gtk.Image()
        advanced_image.set_from_stock(gtk.STOCK_EDIT, 4)
        advanced_image.set_padding(4, 0)
        self.advancedButton.set_alignment(.5, .5)
        self.advancedButton.set_label(language['advanced_settings'])
        self.advancedButton.set_image(advanced_image)
        
        self.scriptButton = gtk.Button()
        script_image = gtk.Image()
        script_image.set_from_icon_name('execute', 4)
        script_image.set_padding(4, 0)
        self.scriptButton.set_alignment(.5 , .5)
        self.scriptButton.set_image(script_image)
        self.scriptButton.set_label(language['scripts'])

        self.checkboxStaticIP = gtk.CheckButton(language['use_static_ip'])
        self.checkboxStaticDNS = gtk.CheckButton(language['use_static_dns'])
        self.checkboxGlobalDNS = gtk.CheckButton(language['use_global_dns'])

        aligner = gtk.Alignment(xscale=1.0)
        aligner.add(self.vboxTop)
        aligner.set_padding(0, 0, 15, 0)
        self.add(aligner)
        
        hboxDNS = gtk.HBox(False, 0)
        hboxDNS.pack_start(self.checkboxStaticDNS)
        hboxDNS.pack_start(self.checkboxGlobalDNS)
        
        self.vboxAdvanced = gtk.VBox(False, 0)
        self.vboxAdvanced.pack_start(self.checkboxStaticIP, fill=False,
                                     expand=False)
        self.vboxAdvanced.pack_start(self.txtIP, fill=False, expand=False)
        self.vboxAdvanced.pack_start(self.txtNetmask, fill=False, expand=False)
        self.vboxAdvanced.pack_start(self.txtGateway, fill=False, expand=False)
        self.vboxAdvanced.pack_start(hboxDNS, fill=False, expand=False)
        self.vboxAdvanced.pack_start(self.txtDNS1, fill=False, expand=False)
        self.vboxAdvanced.pack_start(self.txtDNS2, fill=False, expand=False)
        self.vboxAdvanced.pack_start(self.txtDNS3, fill=False, expand=False)
        
        settings_hbox = gtk.HBox(False, 3)
        settings_hbox.set_border_width(5)
        settings_hbox.pack_start(self.scriptButton, fill=False, expand=False)
        settings_hbox.pack_start(self.advancedButton, fill=False, expand=False)

        self.vboxTop.pack_end(settings_hbox, fill=False, expand=False)

        # Connect the events to the actions
        self.checkboxStaticIP.connect("toggled", self.toggleIPCheckbox)
        self.checkboxStaticDNS.connect("toggled", self.toggleDNSCheckbox)
        self.checkboxGlobalDNS.connect("toggled", self.toggleGlobalDNSCheckbox)

        # Start with all disabled, then they will be enabled later.
        self.checkboxStaticIP.set_active(False)
        self.checkboxStaticDNS.set_active(False)

    def setDefaults(self, widget=None, event=None):
        # After the user types in the IP address,
        # help them out a little.
        ipAddress = self.txtIP.get_text()  # For easy typing :)
        netmask = self.txtNetmask
        gateway = self.txtGateway
        ip_parts = misc.IsValidIP(ipAddress)
        if ip_parts:
            if stringToNone(gateway.get_text()) == None:  # Make sure the gateway box is blank
                # Fill it in with a .1 at the end
                gateway.set_text('.'.join(ip_parts[0:3]) + '.1')

            if stringToNone(netmask.get_text()) == None:  # Make sure the netmask is blank
                        netmask.set_text('255.255.255.0')  # Fill in the most common one
        elif ipAddress != "":
            misc.error(None, "Invalid IP Address Entered.")

    def resetStaticCheckboxes(self):
        # Enable the right stuff
        if not stringToNone(self.txtIP.get_text()) == None:
            self.checkboxStaticIP.set_active(True)
            self.checkboxStaticDNS.set_active(True)
            self.checkboxStaticDNS.set_sensitive(False)
        else:
            self.checkboxStaticIP.set_active(False)
            self.checkboxStaticDNS.set_active(False)
            self.checkboxStaticDNS.set_sensitive(True)

        if not stringToNone(self.txtDNS1.get_text()) == None:
            self.checkboxStaticDNS.set_active(True)
        else:
            self.checkboxStaticDNS.set_active(False)

        #blankify stuff!
        #this will properly disable
        #unused boxes
        self.toggleIPCheckbox()
        self.toggleDNSCheckbox()
        self.toggleGlobalDNSCheckbox()

    def toggleIPCheckbox(self, widget=None):
        # Should disable the static IP text boxes,
        # and also enable the DNS checkbox when
        # disabled and disable when enabled.
        if self.checkboxStaticIP.get_active():
            self.checkboxStaticDNS.set_active(True)
            self.checkboxStaticDNS.set_sensitive(False)
        else:
            self.checkboxStaticDNS.set_sensitive(True)
            self.checkboxStaticDNS.set_active(False)

        self.txtIP.set_sensitive(self.checkboxStaticIP.get_active())
        self.txtNetmask.set_sensitive(self.checkboxStaticIP.get_active())
        self.txtGateway.set_sensitive(self.checkboxStaticIP.get_active())

    def toggleDNSCheckbox(self, widget=None):
        # Should disable the static DNS boxes
        if self.checkboxStaticIP.get_active() == True:
            self.checkboxStaticDNS.set_active(self.checkboxStaticIP.get_active())
            self.checkboxStaticDNS.set_sensitive(False)

        self.checkboxGlobalDNS.set_sensitive(self.checkboxStaticDNS.get_active())
        if self.checkboxStaticDNS.get_active() == True:
            # If global dns is on, don't use local dns
            self.txtDNS1.set_sensitive(not self.checkboxGlobalDNS.get_active())
            self.txtDNS2.set_sensitive(not self.checkboxGlobalDNS.get_active())
            self.txtDNS3.set_sensitive(not self.checkboxGlobalDNS.get_active())
        else:
            self.txtDNS1.set_sensitive(False)
            self.txtDNS2.set_sensitive(False)
            self.txtDNS3.set_sensitive(False)
            self.checkboxGlobalDNS.set_active(False)

    def toggleGlobalDNSCheckbox(self, widget=None):
        if daemon.GetUseGlobalDNS() and self.checkboxStaticDNS.get_active():
            self.txtDNS1.set_sensitive(not self.checkboxGlobalDNS.get_active())
            self.txtDNS2.set_sensitive(not self.checkboxGlobalDNS.get_active())
            self.txtDNS3.set_sensitive(not self.checkboxGlobalDNS.get_active())

class WiredNetworkEntry(NetworkEntry):
    # Creates the wired network expander.
    def __init__(self):
        NetworkEntry.__init__(self)
        self.set_label(language['wired_network'])
        self.resetStaticCheckboxes()
        self.comboProfileNames = gtk.combo_box_entry_new_text()
        self.isFullGUI = True

        self.profileList = config.GetWiredProfileList()
        if self.profileList:  # Make sure there is something in it...
            for x in config.GetWiredProfileList():  # Add all the names to the combobox
                self.comboProfileNames.append_text(x)
        self.hboxTemp = gtk.HBox(False, 0)
        hboxDef = gtk.HBox(False, 0)
        buttonAdd = gtk.Button(stock=gtk.STOCK_ADD)
        buttonDelete = gtk.Button(stock=gtk.STOCK_DELETE)
        self.profileHelp = gtk.Label(language['wired_network_instructions'])
        self.checkboxDefaultProfile = gtk.CheckButton(language['default_wired'])

        self.profileHelp.set_justify(gtk.JUSTIFY_LEFT)
        self.profileHelp.set_line_wrap(True)

        self.vboxTop.pack_start(self.profileHelp, fill=True, expand=True)
        self.hboxTemp.pack_start(self.comboProfileNames, fill=True, expand=True)
        self.hboxTemp.pack_start(buttonAdd, fill=False, expand=False)
        self.hboxTemp.pack_start(buttonDelete, fill=False, expand=False)
        hboxDef.pack_start(self.checkboxDefaultProfile, fill=False, expand=False)

        buttonAdd.connect("clicked", self.addProfile)
        buttonDelete.connect("clicked", self.removeProfile)
        self.comboProfileNames.connect("changed", self.changeProfile)
        self.scriptButton.connect("button-press-event", self.editScripts)
        self.vboxTop.pack_start(hboxDef)
        self.vboxTop.pack_start(self.hboxTemp)

        if stringToBoolean(wired.GetWiredProperty("default")):
            self.checkboxDefaultProfile.set_active(True)
        else:
            self.checkboxDefaultProfile.set_active(False)
        self.checkboxDefaultProfile.connect("toggled", self.toggleDefaultProfile)

        self.show_all()
        self.profileHelp.hide()
        if self.profileList != None:
            prof = config.GetDefaultWiredNetwork()
            if prof != None:  # Make sure the default profile gets displayed.
                i = 0
                while self.comboProfileNames.get_active_text() != prof:
                    self.comboProfileNames.set_active(i)
                    i += 1
            else:
                self.comboProfileNames.set_active(0)
            print "wired profiles found"
            self.set_expanded(False)
        else:
            print "no wired profiles found"
            if not wired.GetAlwaysShowWiredInterface():
                self.set_expanded(True)
            self.profileHelp.show()

    def editScripts(self, widget=None, event=None):
        profile = self.comboProfileNames.get_active_text()
        os.spawnlpe(os.P_WAIT, "gksudo", "gksudo", "./configscript.py",
                    profile, "wired", os.environ)

    def checkEnable(self):
        profileList = config.GetWiredProfileList()
        if profileList == None:
            self.buttonDelete.set_sensitive(False)
            self.higherLevel.connectButton.set_sensitive(False)
            self.vboxAdvanced.set_sensitive(False)

    def addProfile(self, widget):
        print "adding profile"
        profileName = self.comboProfileNames.get_active_text()
        profileList = config.GetWiredProfileList()
        if profileList:
            if profileName in profileList:
                return False
        if profileName != "":
            self.profileHelp.hide()
            config.CreateWiredNetworkProfile(profileName)
            self.comboProfileNames.prepend_text(profileName)
            self.comboProfileNames.set_active(0)
            if self.isFullGUI == True:
                self.buttonDelete.set_sensitive(True)
                self.vboxAdvanced.set_sensitive(True)
                self.higherLevel.connectButton.set_sensitive(True)

    def removeProfile(self, widget):
        print "removing profile"
        config.DeleteWiredNetworkProfile(self.comboProfileNames.get_active_text())
        self.comboProfileNames.remove_text(self.comboProfileNames.get_active())
        self.comboProfileNames.set_active(0)
        if config.GetWiredProfileList() == None:
            self.profileHelp.show()
            entry = self.comboProfileNames.child
            entry.set_text("")
            if self.isFullGUI == True:
                self.buttonDelete.set_sensitive(False)
                self.vboxAdvanced.set_sensitive(False)
                self.higherLevel.connectButton.set_sensitive(False)
        else:
            self.profileHelp.hide()

    def toggleDefaultProfile(self, widget):
        if self.checkboxDefaultProfile.get_active():
            print 'unsetting previous default profile...'
            # Make sure there is only one default profile at a time
            config.UnsetWiredDefault()
        wired.SetWiredProperty("default",
                               self.checkboxDefaultProfile.get_active())
        config.SaveWiredNetworkProfile(self.comboProfileNames.get_active_text())

    def changeProfile(self, widget):
        # Make sure the name doesn't change everytime someone types something
        if self.comboProfileNames.get_active() > -1:
            if self.isFullGUI == False:
                return
            print "changing profile..."
            profileName = self.comboProfileNames.get_active_text()
            print profileName
            config.ReadWiredNetworkProfile(profileName)

            self.txtIP.set_text(self.format_entry("ip"))
            self.txtNetmask.set_text(self.format_entry("netmask"))
            self.txtGateway.set_text(self.format_entry("gateway"))

            self.txtDNS1.set_text(self.format_entry("dns1"))
            self.txtDNS2.set_text(self.format_entry("dns2"))
            self.txtDNS3.set_text(self.format_entry("dns3"))

            is_default = wired.GetWiredProperty("default")
            self.checkboxDefaultProfile.set_active(stringToBoolean(is_default))
            self.resetStaticCheckboxes()

    def format_entry(self, label):
        return noneToBlankString(wired.GetWiredProperty(label))

class WirelessNetworkEntry(NetworkEntry):
    # This class is respsponsible for creating the expander
    # in each wirelessnetwork entry.
    def __init__(self, networkID):
        self.networkID = networkID
        # Create the data labels
        NetworkEntry.__init__(self)
        self.essid = wireless.GetWirelessProperty(networkID, "essid")
        print "ESSID : " + self.essid
        self.set_label(self.essid)

        # Make the vbox to hold the encryption stuff.
        self.vboxEncryptionInformation = gtk.VBox(False, 0)
        # Make the combo box.
        self.comboEncryption = gtk.combo_box_new_text()
        self.checkboxEncryption = gtk.CheckButton(language['use_encryption'])
        self.lblStrength = GreyLabel()
        self.lblEncryption = GreyLabel()
        self.lblMAC = GreyLabel()
        self.lblChannel = GreyLabel()
        self.lblMode = GreyLabel()
        self.hboxStatus = gtk.HBox(False, 5)
        self.checkboxAutoConnect = gtk.CheckButton(language['automatic_connect'])
        self.checkboxAutoConnect.connect("toggled", self.updateAutoConnect)

        self.hboxStatus.pack_start(self.lblStrength, fill=False, expand=True)
        self.hboxStatus.pack_start(self.lblEncryption, fill=False, expand=True)
        self.hboxStatus.pack_start(self.lblMAC, fill=False, expand=True)
        self.hboxStatus.pack_start(self.lblMode, fill=False, expand=True)
        self.hboxStatus.pack_start(self.lblChannel, fill=False, expand=True)

        self.vboxTop.pack_start(self.checkboxAutoConnect, fill=False, 
                                expand=False)
        self.vboxTop.pack_start(self.hboxStatus, fill=True, expand=True)
        
        self.vboxAdvanced.pack_start(self.checkboxEncryption, fill=False,
                                     expand=False)

        self.txtIP.set_text(self.format_entry(networkID,"ip"))
        self.txtNetmask.set_text(self.format_entry(networkID,"netmask"))
        self.txtGateway.set_text(self.format_entry(networkID,"gateway"))

        if wireless.GetWirelessProperty(networkID,'use_global_dns'):
            self.checkboxGlobalDNS.set_active(True)

        if wireless.GetWirelessProperty(networkID,"dns1") != None:
            self.txtDNS1.set_text(self.format_entry(networkID,"dns1"))

        if wireless.GetWirelessProperty(networkID,'dns2') != None:
            self.txtDNS2.set_text(self.format_entry(networkID,"dns2"))

        if wireless.GetWirelessProperty(networkID,'dns3') != None:
            self.txtDNS3.set_text(self.format_entry(networkID,"dns3"))

        self.resetStaticCheckboxes()
        encryptionTypes = misc.LoadEncryptionMethods()

        self.checkboxEncryption.set_active(False)
        self.comboEncryption.set_sensitive(False)

        if stringToBoolean(self.format_entry(networkID, "automatic")):
            self.checkboxAutoConnect.set_active(True)
        else:
            self.checkboxAutoConnect.set_active(False)
        #set it up right, with disabled stuff
        self.toggleEncryption()

        #add the names to the menu
        activeID = -1 #set the menu to this item when we are done
        for x in encryptionTypes:
            self.comboEncryption.append_text(encryptionTypes[x][0])
            if encryptionTypes[x][1] == wireless.GetWirelessProperty(networkID,
                                                                     "enctype"):
                activeID = x

        self.comboEncryption.set_active(activeID)
        if activeID != -1:
            self.checkboxEncryption.set_active(True)
            self.comboEncryption.set_sensitive(True)
            self.vboxEncryptionInformation.set_sensitive(True)
        else:
            self.comboEncryption.set_active(0)

        self.vboxAdvanced.pack_start(self.comboEncryption)
        self.vboxAdvanced.pack_start(self.vboxEncryptionInformation)
        self.changeEncryptionMethod()
        self.scriptButton.connect("button-press-event", self.editScripts)
        self.checkboxEncryption.connect("toggled", self.toggleEncryption)
        self.comboEncryption.connect("changed", self.changeEncryptionMethod)
        self.show_all()

    def format_entry(self, networkid, label):
        return noneToBlankString(wireless.GetWirelessProperty(networkid, label))

    def editScripts(self, widget=None, event=None):
        result = os.spawnlpe(os.P_WAIT, "gksudo", "gksudo", "./configscript.py",
                   str(self.networkID), "wireless", os.environ)
        print result

    def updateAutoConnect(self, widget=None):
        wireless.SetWirelessProperty(self.networkID, "automatic",
                                     noneToString(self.checkboxAutoConnect.get_active()))
        
        config.SaveWirelessNetworkProperty(self.networkID, "automatic")

    def toggleEncryption(self, widget=None):
        active = self.checkboxEncryption.get_active()
        self.vboxEncryptionInformation.set_sensitive(active)
        self.comboEncryption.set_sensitive(active)

    def changeEncryptionMethod(self, widget=None):
        for z in self.vboxEncryptionInformation:
            z.destroy()  # Remove stuff in there already
        ID = self.comboEncryption.get_active()
        methods = misc.LoadEncryptionMethods()
        self.encryptionInfo = {}
        if ID == -1:
            #in case nothing is selected
            self.comboEncryption.set_active(0)
            ID == 0
        for x in methods[ID][2]:
            box = None
            if language.has_key(methods[ID][2][x][0]):
                box = LabelEntry(language[methods[ID][2][x][0].lower().replace(' ','_')])
            else:
                box = LabelEntry(methods[ID][2][x][0].replace('_',' '))
            box.set_auto_hidden(True)
            self.vboxEncryptionInformation.pack_start(box)
            #add the data to any array, so that the information
            #can be easily accessed by giving the name of the wanted
            #data
            self.encryptionInfo[methods[ID][2][x][1]] = box.entry

            box.entry.set_text(noneToBlankString(
                wireless.GetWirelessProperty(self.networkID,methods[ID][2][x][1])))
        self.vboxEncryptionInformation.show_all()

    def setSignalStrength(self, strength, dbm_strength):
        display_type = daemon.GetSignalDisplayType()
        if daemon.GetWPADriver() == 'ralink legacy' or display_type == 1:
            ending = "dBm"
            disp_strength = str(dbm_strength)
        else:
            ending = "%"
            disp_strength = str(strength)
        self.lblStrength.set_label(disp_strength + ending)

    def setMACAddress(self, address):
        self.lblMAC.set_label(str(address))

    def setEncryption(self, on, ttype):
        if on and ttype:
            self.lblEncryption.set_label(str(ttype))
        if on and not ttype: 
            self.lblEncryption.set_label(language['secured'])
        if not on:
            self.lblEncryption.set_label(language['unsecured'])

    def setChannel(self, channel):
        self.lblChannel.set_label(language['channel'] + ' ' + str(channel))

    def setMode(self, mode):
        self.lblMode.set_label(str(mode))

class WiredProfileChooser:
    """ Class for displaying the wired profile chooser. """
    def __init__(self):
        """ Initializes and runs the wired profile chooser. """
        # Import and init WiredNetworkEntry to steal some of the
        # functions and widgets it uses.
        wiredNetEntry = WiredNetworkEntry()
        #wiredNetEntry.__init__()

        dialog = gtk.Dialog(title = language['wired_network_found'],
                            flags = gtk.DIALOG_MODAL,
                            buttons = (gtk.STOCK_CONNECT, 1,
                                       gtk.STOCK_CANCEL, 2))
        dialog.set_has_separator(False)
        dialog.set_size_request(400, 150)
        instructLabel = gtk.Label(language['choose_wired_profile'] + ':\n')
        stoppopcheckbox = gtk.CheckButton(language['stop_showing_chooser'])

        wiredNetEntry.isFullGUI = False
        instructLabel.set_alignment(0, 0)
        stoppopcheckbox.set_active(False)

        # Remove widgets that were added to the normal
        # WiredNetworkEntry so that they can be added to
        # the pop-up wizard.
        wiredNetEntry.vboxTop.remove(wiredNetEntry.hboxTemp)
        wiredNetEntry.vboxTop.remove(wiredNetEntry.profileHelp)

        dialog.vbox.pack_start(instructLabel, fill=False, expand=False)
        dialog.vbox.pack_start(wiredNetEntry.profileHelp, fill=False,
                               expand=False)
        dialog.vbox.pack_start(wiredNetEntry.hboxTemp, fill=False,
                               expand=False)
        dialog.vbox.pack_start(stoppopcheckbox, fill=False, expand=False)
        dialog.show_all()

        wired_profiles = wiredNetEntry.comboProfileNames
        wiredNetEntry.profileHelp.hide()
        if wiredNetEntry.profileList != None:
            wired_profiles.set_active(0)
            print "wired profiles found"
        else:
            print "no wired profiles found"
            wiredNetEntry.profileHelp.show()

        response = dialog.run()
        if response == 1:
            print 'reading profile ', wired_profiles.get_active_text()
            config.ReadWiredNetworkProfile(wired_profiles.get_active_text())
            wired.ConnectWired()
        else:
            if stoppopcheckbox.get_active():
                daemon.SetForcedDisconnect(True)
        dialog.destroy()


class appGui:
    """ The main wicd GUI class. """
    def __init__(self):
        """ Initializes everything needed for the GUI. """
        gladefile = "data/wicd.glade"
        self.windowname = "gtkbench"
        self.wTree = gtk.glade.XML(gladefile)

        dic = { "refresh_clicked" : self.refresh_networks, 
                "quit_clicked" : self.exit, 
                "disconnect_clicked" : self.disconnect,
                "main_exit" : self.exit, 
                "cancel_clicked" : self.cancel_connect,
                "connect_clicked" : self.connect_hidden,
                "preferences_clicked" : self.settings_dialog,
                "about_clicked" : self.about_dialog,
                "create_adhoc_network_button_button" : self.create_adhoc_network}
        self.wTree.signal_autoconnect(dic)

        # Set some strings in the GUI - they may be translated
        label_instruct = self.wTree.get_widget("label_instructions")
        label_instruct.set_label(language['select_a_network'])

        probar = self.wTree.get_widget("progressbar")
        probar.set_text(language['connecting'])
        
        self.window = self.wTree.get_widget("window1")
        self.network_list = self.wTree.get_widget("network_list_vbox")
        self.status_area = self.wTree.get_widget("connecting_hbox")
        self.status_bar = self.wTree.get_widget("statusbar")
        self.refresh_networks(fresh=False)

        self.status_area.hide_all()

        self.statusID = None
        self.first_dialog_load = False
        self.vpn_connection_pipe = None
        self.is_visible = True
        
        self.window.connect('delete_event', self.exit)

        size = config.ReadWindowSize()
        width = size[0]
        height = size[1]
        if width > -1 and height > -1:
            self.window.resize(int(width), int(height))

        gobject.timeout_add(600, self.update_statusbar)
        gobject.timeout_add(100, self.pulse_progress_bar)

    def create_adhoc_network(self, widget=None):
        """ Shows a dialog that creates a new adhoc network. """
        print "Starting the Ad-Hoc Network Creation Process..."
        dialog = gtk.Dialog(title = language['create_adhoc_network'],
                            flags = gtk.DIALOG_MODAL,
                            buttons=(gtk.STOCK_OK, 1, gtk.STOCK_CANCEL, 2))
        dialog.set_has_separator(False)
        dialog.set_size_request(400, -1)
        self.useEncryptionCheckbox = gtk.CheckButton(language['use_wep_encryption'])
        self.useEncryptionCheckbox.set_active(False)
        ipEntry = LabelEntry(language['ip'] + ':')
        essidEntry = LabelEntry(language['essid'] + ':')
        channelEntry = LabelEntry(language['channel'] + ':')
        self.keyEntry = LabelEntry(language['key'] + ':')
        self.keyEntry.set_auto_hidden(True)
        self.keyEntry.set_sensitive(False)

        useICSCheckbox = gtk.CheckButton(language['use_ics'])

        self.useEncryptionCheckbox.connect("toggled",
                                           self.toggleEncryptionCheck)
        channelEntry.entry.set_text('3')
        essidEntry.entry.set_text('My_Adhoc_Network')
        ipEntry.entry.set_text('169.254.12.10') #Just a random IP

        vboxA = gtk.VBox(False, 0)
        vboxA.pack_start(self.useEncryptionCheckbox, fill=False, expand=False)
        vboxA.pack_start(self.keyEntry, fill=False, expand=False)
        vboxA.show()
        dialog.vbox.pack_start(essidEntry)
        dialog.vbox.pack_start(ipEntry)
        dialog.vbox.pack_start(channelEntry)
        dialog.vbox.pack_start(useICSCheckbox)
        dialog.vbox.pack_start(vboxA)
        dialog.vbox.set_spacing(5)
        dialog.show_all()
        response = dialog.run()
        if response == 1:
            wireless.CreateAdHocNetwork(essidEntry.entry.get_text(),
                                        channelEntry.entry.get_text(),
                                        ipEntry.entry.get_text(), "WEP",
                                        self.keyEntry.entry.get_text(),
                                        self.useEncryptionCheckbox.get_active(),
                                        False) #useICSCheckbox.get_active())
        dialog.destroy()
        
    def toggleEncryptionCheck(self, widget=None):
        """ Toggles the encryption key entry box for the ad-hoc dialog. """
        self.keyEntry.set_sensitive(self.useEncryptionCheckbox.get_active())

    def disconnect(self, widget=None):
        """ Disconnects from any active network. """
        daemon.Disconnect()

    def about_dialog(self, widget, event=None):
        """ Displays an about dialog. """
        dialog = gtk.AboutDialog()
        dialog.set_name("Wicd")
        dialog.set_version(daemon.Hello())
        dialog.set_authors([ "Adam Blackburn", "Dan O'Reilly" ])
        dialog.set_website("http://wicd.sourceforge.net")
        dialog.run()
        dialog.destroy()

    def settings_dialog(self, widget, event=None):
        """ Displays a general settings dialog. """
        dialog = self.wTree.get_widget("pref_dialog")
        dialog.set_title(language['preferences'])
        wiredcheckbox = self.wTree.get_widget("pref_always_check")
        wiredcheckbox.set_label(language['wired_always_on'])
        wiredcheckbox.set_active(wired.GetAlwaysShowWiredInterface())
        
        reconnectcheckbox = self.wTree.get_widget("pref_auto_check")
        reconnectcheckbox.set_label(language['auto_reconnect'])
        reconnectcheckbox.set_active(daemon.GetAutoReconnect())

        debugmodecheckbox = self.wTree.get_widget("pref_debug_check")
        debugmodecheckbox.set_label(language['use_debug_mode'])
        debugmodecheckbox.set_active(daemon.GetDebugMode())

        displaytypecheckbox = self.wTree.get_widget("pref_dbm_check")
        displaytypecheckbox.set_label(language['display_type_dialog'])
        displaytypecheckbox.set_active(daemon.GetSignalDisplayType())

        entryWiredAutoMethod = self.wTree.get_widget("pref_wired_auto_label")
        entryWiredAutoMethod.set_label('Wired Autoconnect Setting:')
        usedefaultradiobutton = self.wTree.get_widget("pref_use_def_radio")
        usedefaultradiobutton.set_label(language['use_default_profile'])
        showlistradiobutton = self.wTree.get_widget("pref_prompt_radio")
        showlistradiobutton.set_label(language['show_wired_list'])
        lastusedradiobutton = self.wTree.get_widget("pref_use_last_radio")
        lastusedradiobutton.set_label(language['use_last_used_profile'])
        
        if wired.GetWiredAutoConnectMethod() == 1:
            usedefaultradiobutton.set_active(True)
        elif wired.GetWiredAutoConnectMethod() == 2:
            showlistradiobutton.set_active(True)
        elif wired.GetWiredAutoConnectMethod() == 3:
            lastusedradiobutton.set_active(True)

        self.set_label("pref_driver_label", language['wpa_supplicant_driver'] +
                       ':')
        # Hack to get the combo box we need, which you can't do with glade.
        if not self.first_dialog_load:
            self.first_dialog_load = True
            wpa_hbox = self.wTree.get_widget("hbox_wpa")
            wpadrivercombo = gtk.combo_box_new_text()
            wpa_hbox.pack_end(wpadrivercombo)
            
        wpadrivers = ["hostap", "hermes", "madwifi", "atmel", "wext",
                      "ndiswrapper", "broadcom", "ipw", "ralink legacy"]
        i = 0
        found = False
        for x in wpadrivers:
            if x == daemon.GetWPADriver() and not found:
                found = True
            elif not found:
                i += 1
            wpadrivercombo.append_text(x)

        # Set the active choice here.  Doing it before all the items are
        # added the combobox causes the choice to be reset.
        wpadrivercombo.set_active(i)
        if not found:
            # Use wext as default, since normally it is the correct driver.
            wpadrivercombo.set_active(4)

        self.set_label("pref_wifi_label", language['wireless_interface'] + ':')
        self.set_label("pref_wired_label", language['wired_interface'] + ':')

        entryWirelessInterface = self.wTree.get_widget("pref_wifi_entry")
        entryWirelessInterface.set_text(daemon.GetWirelessInterface())

        entryWiredInterface = self.wTree.get_widget("pref_wired_entry")
        entryWiredInterface.set_text(daemon.GetWiredInterface())

        # Set up global DNS stuff
        useGlobalDNSCheckbox = self.wTree.get_widget("pref_global_check")
        useGlobalDNSCheckbox.set_label(language['use_global_dns'])
        
        dns1Entry = self.wTree.get_widget("pref_dns1_entry")
        dns2Entry = self.wTree.get_widget("pref_dns2_entry")
        dns3Entry = self.wTree.get_widget("pref_dns3_entry")
        self.set_label("pref_dns1_label", language['dns'] + ' ' + language['1'])
        self.set_label("pref_dns2_label", language['dns'] + ' ' + language['2'])
        self.set_label("pref_dns3_label", language['dns'] + ' ' + language['3'])

        useGlobalDNSCheckbox.connect("toggled", checkboxTextboxToggle,
                                     (dns1Entry, dns2Entry, dns3Entry))

        dns_addresses = daemon.GetGlobalDNSAddresses()
        useGlobalDNSCheckbox.set_active(daemon.GetUseGlobalDNS())
        dns1Entry.set_text(noneToBlankString(dns_addresses[0]))
        dns2Entry.set_text(noneToBlankString(dns_addresses[1]))
        dns3Entry.set_text(noneToBlankString(dns_addresses[2]))

        if not daemon.GetUseGlobalDNS():
            dns1Entry.set_sensitive(False)
            dns2Entry.set_sensitive(False)
            dns3Entry.set_sensitive(False)

        # Bold/Align the Wired Autoconnect label.
        entryWiredAutoMethod.set_alignment(0, 0)
        atrlist = pango.AttrList()
        atrlist.insert(pango.AttrWeight(pango.WEIGHT_BOLD, 0, 50))
        entryWiredAutoMethod.set_attributes(atrlist)
        dialog.show_all()

        response = dialog.run()
        if response == 1:
            daemon.SetUseGlobalDNS(useGlobalDNSCheckbox.get_active())
            daemon.SetGlobalDNS(dns1Entry.get_text(), dns2Entry.get_text(),
                                dns3Entry.get_text())
            daemon.SetWirelessInterface(entryWirelessInterface.get_text())
            daemon.SetWiredInterface(entryWiredInterface.get_text())
            print "setting: " + wpadrivers[wpadrivercombo.get_active()]
            daemon.SetWPADriver(wpadrivers[wpadrivercombo.get_active()])
            wired.SetAlwaysShowWiredInterface(wiredcheckbox.get_active())
            daemon.SetAutoReconnect(reconnectcheckbox.get_active())
            daemon.SetDebugMode(debugmodecheckbox.get_active())
            daemon.SetSignalDisplayType(displaytypecheckbox.get_active())
            if showlistradiobutton.get_active():
                wired.SetWiredAutoConnectMethod(2)
            elif lastusedradiobutton.get_active():
                wired.SetWiredAutoConnectMethod(3)
            else:
                wired.SetWiredAutoConnectMethod(1)
        dialog.hide()

    def set_label(self, glade_str, label):
        """ Sets the label for the given widget in wicd.glade. """
        self.wTree.get_widget(glade_str).set_label(label)

    def connect_hidden(self, widget):
        """ Prompts the user for a hidden network, then scans for it. """
        # Should display a dialog asking
        # for the ssid of a hidden network
        # and displaying connect/cancel buttons
        dialog = gtk.Dialog(title=language['hidden_network'], flags=gtk.DIALOG_MODAL,
                            buttons=(gtk.STOCK_CONNECT, 1, gtk.STOCK_CANCEL, 2))
        dialog.set_has_separator(False)
        dialog.lbl = gtk.Label(language['hidden_network_essid'])
        dialog.textbox = gtk.Entry()
        dialog.vbox.pack_start(dialog.lbl)
        dialog.vbox.pack_start(dialog.textbox)
        dialog.show_all()
        button = dialog.run()
        if button == 1:
            answer = dialog.textbox.get_text()
            dialog.destroy()
            self.refresh_networks(None, True, answer)
        else:
            dialog.destroy()

    def cancel_connect(self, widget):
        """ Alerts the daemon to cancel the connection process. """
        #should cancel a connection if there
        #is one in progress
        cancelButton = self.wTree.get_widget("cancel_button")
        cancelButton.set_sensitive(False)
        daemon.CancelConnect()
        # Prevents automatic reconnecting if that option is enabled
        daemon.SetForcedDisconnect(True)

    def pulse_progress_bar(self):
        """ Pulses the progress bar while connecting to a network. """
        if not self.is_visible:
            return True
        try:
            self.wTree.get_widget("progressbar").pulse()
        except:
            pass
        return True

    def update_statusbar(self):
        """ Updates the status bar. """
        if self.is_visible == False:
            return True

        iwconfig = wireless.GetIwconfig()
        wireless_ip = wireless.GetWirelessIP()
        wiredConnecting = wired.CheckIfWiredConnecting()
        wirelessConnecting = wireless.CheckIfWirelessConnecting()
        
        if wirelessConnecting or wiredConnecting:
            self.network_list.set_sensitive(False)
            self.status_area.show_all()
            if self.statusID:
                self.status_bar.remove(1, self.statusID)
            if wirelessConnecting:
                self.set_status(wireless.GetCurrentNetwork(iwconfig) + ': ' +
                                language[str(wireless.CheckWirelessConnectingMessage())])
            if wiredConnecting:
                self.set_status(language['wired_network'] + ': ' + 
                                language[str(wired.CheckWiredConnectingMessage())])
        else:
            self.network_list.set_sensitive(True)
            self.status_area.hide_all()
            if self.statusID:
                self.status_bar.remove(1, self.statusID)

            # Determine connection status.
            if self.check_for_wireless(iwconfig, wireless_ip):
                return True

            wired_ip = wired.GetWiredIP()
            if self.check_for_wired(wired_ip):
                return True
            
            self.set_status(language['not_connected'])
        return True
    
    def check_for_wired(self, wired_ip):
        """ Determine if wired is active, and if yes, set the status. """
        if wired_ip and wired.CheckPluggedIn():
            self.set_status(language['connected_to_wired'].replace('$A',
                                                                   wired_ip))
            return True
        else:
            return False
        
    def check_for_wireless(self, iwconfig, wireless_ip):
        """ Determine if wireless is active, and if yes, set the status. """
        if not wireless_ip:
            return False
        
        network = wireless.GetCurrentNetwork(iwconfig)
        if not network:
            return False
    
        strength = wireless.GetCurrentSignalStrength(iwconfig)
        dbm_strength = wireless.GetCurrentDBMStrength(iwconfig)
        if strength is not None and dbm_strength is not None:
            network = str(network)
            if daemon.GetSignalDisplayType() == 0:
                strength = str(strength)
            else:
                strength = str(dbm_strength)
            ip = str(wireless_ip)
            self.set_status(language['connected_to_wireless'].replace
                            ('$A', network).replace
                            ('$B', daemon.FormatSignalForPrinting(strength)).replace
                            ('$C', wireless_ip))
            return True
        return False

    def set_status(self, msg):
        """ Sets the status bar message for the GUI. """
        self.statusID = self.status_bar.push(1, msg)

    def refresh_networks(self, widget=None, fresh=True, hidden=None):
        """ Refreshes the network list.
        
        If fresh=True, scans for wireless networks and displays the results.
        If a ethernet connection is available, or the user has chosen to,
        displays a Wired Network entry as well.
        If hidden isn't None, will scan for networks after running
        iwconfig <wireless interface> essid <hidden>.
        
        """
        print "refreshing..."

        printLine = False  # We don't print a separator by default.
        # Remove stuff already in there.
        for z in self.network_list:
            z.destroy()

        if wired.CheckPluggedIn() or wired.GetAlwaysShowWiredInterface():
            printLine = True  # In this case we print a separator.
            wirednet = PrettyWiredNetworkEntry()
            self.network_list.pack_start(wirednet, fill=False, expand=False)
            wirednet.connectButton.connect("button-press-event", self.connect,
                                           "wired", 0, wirednet)
            wirednet.expander.advancedButton.connect("button-press-event",
                                                     self.edit_advanced,
                                                     "wired", 0, wirednet)
        # Scan
        if fresh:
            # Even if it is None, it can still be passed.
            wireless.SetHiddenNetworkESSID(noneToString(hidden))
            wireless.Scan()

        num_networks = wireless.GetNumberOfNetworks()

        instructLabel = self.wTree.get_widget("label_instructions")
        if num_networks > 0:
            instructLabel.show()
            for x in range(0, num_networks):
                if printLine:
                    sep = gtk.HSeparator()
                    self.network_list.pack_start(sep, padding=10, expand=False,
                                                 fill=False)
                    sep.show()
                else:
                    printLine = True
                tempnet = PrettyWirelessNetworkEntry(x)
                tempnet.show_all()
                self.network_list.pack_start(tempnet, expand=False, fill=False)
                tempnet.connectButton.connect("button-press-event",
                                               self.connect, "wireless", x,
                                               tempnet)
                tempnet.expander.advancedButton.connect("button-press-event",
                                                        self.edit_advanced,
                                                        "wireless", x, tempnet)
        else:
            instructLabel.hide()
            if wireless.GetKillSwitchEnabled():
                label = gtk.Label(language['killswitch_enabled'] + ".")
            else:
                label = gtk.Label(language['no_wireless_networks_found'])
            self.network_list.pack_start(label)
            label.show()

    def save_settings(self, nettype, networkid, networkentry):
        """ Verifies and saves the settings for the network entry. """
        entry = networkentry.expander
        entlist = []
        
        # First make sure all the Addresses entered are valid.
        if entry.checkboxStaticIP.get_active():
            for ent in [entry.txtIP, entry.txtNetmask, entry.txtGateway]:
                entlist.append(ent)
                
        if entry.checkboxStaticDNS.get_active() and \
           not entry.checkboxGlobalDNS.get_active():
            entlist.append(entry.txtDNS1)
            # Only append addition dns entries if they're entered.
            for ent in [entry.txtDNS2, entry.txtDNS3]:
                if ent.get_text() != "":
                    entlist.append(ent)
                    
        for lblent in entlist:
            if not misc.IsValidIP(lblent.get_text()):
                misc.error(self.window, language['invalid_address'].
                                        replace('$A', lblent.label.get_label()))
                return False

        # Now save the settings.
        if nettype == "wireless":
            self.save_wireless_settings(networkid, entry)

        elif nettype == "wired":
            self.save_wired_settings(entry)
            
        return True
    
    def save_wired_settings(self, entry):
            if entry.checkboxStaticIP.get_active():
                wired.SetWiredProperty("ip", noneToString(entry.txtIP.get_text()))
                wired.SetWiredProperty("netmask", noneToString(entry.txtNetmask.get_text()))
                wired.SetWiredProperty("gateway", noneToString(entry.txtGateway.get_text()))
            else:
                wired.SetWiredProperty("ip", '')
                wired.SetWiredProperty("netmask", '')
                wired.SetWiredProperty("gateway", '')

            if entry.checkboxStaticDNS.get_active() and \
               not entry.checkboxGlobalDNS.get_active():
                wired.SetWiredProperty('use_static_dns', True)
                wired.SetWiredProperty('use_global_dns', False)
                wired.SetWiredProperty("dns1", noneToString(entry.txtDNS1.get_text()))
                wired.SetWiredProperty("dns2", noneToString(entry.txtDNS2.get_text()))
                wired.SetWiredProperty("dns3", noneToString(entry.txtDNS3.get_text()))
            elif entry.checkboxStaticDNS.get_active() and \
                 entry.checkboxGlobalDNS.get_active():
                wired.SetWiredProperty('use_static_dns', True)
                wired.SetWiredProperty('use_global_dns', True)
            else:
                wired.SetWiredProperty('use_static_dns', False)
                wired.SetWiredProperty("dns1", '')
                wired.SetWiredProperty("dns2", '')
                wired.SetWiredProperty("dns3", '')
            config.SaveWiredNetworkProfile(entry.comboProfileNames.get_active_text())
            
    def save_wireless_settings(self, networkid, entry):
        print 'networkid', networkid
        wireless.SetWirelessProperty(networkid, "automatic",
                                     noneToString(entry.checkboxAutoConnect.get_active()))
     
        if entry.checkboxStaticIP.get_active():
            wireless.SetWirelessProperty(networkid, "ip",
                                      noneToString(entry.txtIP.get_text()))
            wireless.SetWirelessProperty(networkid, "netmask",
                                         noneToString(entry.txtNetmask.get_text()))
            wireless.SetWirelessProperty(networkid, "gateway",
                                         noneToString(entry.txtGateway.get_text()))
        else:
            # Blank the values
            wireless.SetWirelessProperty(networkid, "ip", '')
            wireless.SetWirelessProperty(networkid, "netmask", '')
            wireless.SetWirelessProperty(networkid, "gateway", '')
   
        if entry.checkboxStaticDNS.get_active() and \
           not entry.checkboxGlobalDNS.get_active():
            wireless.SetWirelessProperty(networkid, 'use_static_dns', True)
            wireless.SetWirelessProperty(networkid, 'use_global_dns', False)
            wireless.SetWirelessProperty(networkid, 'dns1',
                                         noneToString(entry.txtDNS1.get_text()))
            wireless.SetWirelessProperty(networkid, 'dns2',
                                         noneToString(entry.txtDNS2.get_text()))
            wireless.SetWirelessProperty(networkid, 'dns3',
                                         noneToString(entry.txtDNS3.get_text()))
        elif entry.checkboxStaticDNS.get_active() and \
             entry.checkboxGlobalDNS.get_active():
            wireless.SetWirelessProperty(networkid, 'use_static_dns', True)
            wireless.SetWirelessProperty(networkid, 'use_global_dns', True)
        else:
            wireless.SetWirelessProperty(networkid, 'use_static_dns', False) 
            wireless.SetWirelessProperty(networkid, 'use_global_dns', False)
            wireless.SetWirelessProperty(networkid, 'dns1', '')
            wireless.SetWirelessProperty(networkid, 'dns2', '')
            wireless.SetWirelessProperty(networkid, 'dns3', '')
   
        if entry.checkboxEncryption.get_active():
            print "setting encryption info..."
            encryptionInfo = entry.encryptionInfo
            encrypt_methods = misc.LoadEncryptionMethods()
            wireless.SetWirelessProperty(networkid, "enctype",
                                         encrypt_methods[entry.comboEncryption.
                                                         get_active()][1])
            for x in encryptionInfo:
                wireless.SetWirelessProperty(networkid, x,
                                             noneToString(encryptionInfo[x].get_text()))
        else:
            print "no encryption specified..."
            wireless.SetWirelessProperty(networkid, "enctype", "None")
            
        config.SaveWirelessNetworkProfile(networkid)

    def edit_advanced(self, widget, event, ttype, networkid, networkentry):
        """ Display the advanced settings dialog.
        
        Displays the advanced settings dialog and saves any changes made.
        If errors occur in the settings, an error message will be displayed
        and the user won't be able to save the changes until the errors
        are fixed.
        
        """
        dialog = gtk.Dialog(title=language['advanced_settings'],
                            flags=gtk.DIALOG_MODAL, buttons=(gtk.STOCK_OK,
                                                          gtk.RESPONSE_ACCEPT,
                                                          gtk.STOCK_CANCEL,
                                                          gtk.RESPONSE_REJECT))
        dialog.vbox.pack_start(networkentry.expander.vboxAdvanced)
        dialog.show_all()
        while True:
            if self.run_settings_dialog(dialog, ttype, networkid, networkentry):
                break
        dialog.vbox.remove(networkentry.expander.vboxAdvanced)
        dialog.destroy()
        
    def run_settings_dialog(self, dialog, nettype, networkid, networkentry):
        """ Runs the settings dialog.
        
        Runs the settings dialog and returns True if settings are saved
        successfully, and false otherwise.
        
        """
        result = dialog.run()
        if result == gtk.RESPONSE_ACCEPT:
            if self.save_settings(nettype, networkid, networkentry):
                return True
            else:
                return False
        return True

    def connect(self, widget, event, nettype, networkid, networkentry):
        """ Initiates the connection process in the daemon. """
        cancelButton = self.wTree.get_widget("cancel_button")
        cancelButton.set_sensitive(True)
        
        if not self.save_settings(nettype, networkid, networkentry):
            return False
        
        if nettype == "wireless":
            wireless.ConnectWireless(networkid)
        elif nettype == "wired":
            wired.ConnectWired()

    def exit(self, widget=None, event=None):
        """ Hide the wicd GUI.
        
        This method hides the wicd GUI and writes the current window size
        to disc for later use.  This method does NOT actually destroy the
        GUI, it just hides it.
        
        """
        self.window.hide()
        self.is_visible = False
        [width, height] = self.window.get_size()
        config.WriteWindowSize(width, height)
        daemon.SetGUIOpen(False)
        while gtk.events_pending():
            gtk.main_iteration()
        return True

    def show_win(self):
        """ Brings the GUI out of the hidden state. 
        
        Method to show the wicd GUI, alert the daemon that it is open,
        and refresh the network list.
        
        """
        self.window.show()
        self.is_visible = True
        daemon.SetGUIOpen(True)
        self.refresh_networks()
        
        
if __name__ == '__main__':
    app = appGui()
    gtk.main()
