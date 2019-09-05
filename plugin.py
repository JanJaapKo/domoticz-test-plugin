# Basic Python Plugin Example
#
# Author: Jan-Jaap Kostelijk
#
"""
<plugin key="tetsPlugIn" name="test plugin" author="Jan-Jaap Kostelijk" version="1.1.0" >
    <description>
        Test plugin<br/><br/>
        just a plugin to run some simple tests<br/>
        now setup to test Dyson cloud account connection
    </description>
    <params>
		<param field="Address" label="IP Address" width="200px" required="true" default="192.168.86.23"/>
		<param field="Port" label="Port" width="30px" required="true" default="1883"/>
		<param field="Username" label="Username" default="bla" required="true"/>
		<param field="Password" label="Password" required="true" password="true"/>
        <param field="Mode3" label="Dyson password" width="300px" required="false" default=""/>
		<param field="Mode5" label="email adress" default="sinterklaas@gmail.com" required="true"/>
		<param field="Mode4" label="Debug" width="75px">
            <options>
                <option label="Verbose" value="Verbose"/>
                <option label="True" value="Debug" default="true"/>
                <option label="False" value="Normal"/>
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import time
import base64, hashlib
from dyson import DysonAccount

class TestPlug:
    #define class variables

    def __init__(self):
        pass

    def onStart(self):
        Domoticz.Log("onStart called")
        if Parameters['Mode4'] == 'Debug':
            Domoticz.Debugging(1)
            DumpConfigToLog()
        if Parameters['Mode4'] == 'Verbose':
            Domoticz.Debugging(2+4+8+16+64)
            DumpConfigToLog()

        #read out parameters
        Domoticz.Debug("Password field: " + Parameters['Password'])
        Domoticz.Debug("Password 2 field: " + Parameters['Mode3'])
        #self.password = self._hashed_password(Parameters['Password'])
        #Domoticz.Debug("Password 2 field: hashed " + self.password)
        #Parameters['Password'] = self.password
        #Domoticz.Debug("Password field: hashed????? " + Parameters['Password'])
        
        #create a Dyson account
        Domoticz.Debug("=== start making connection to Dyson account ===")
        dysonAccount = DysonAccount(Parameters['Mode5'],Parameters['Mode3'],"NL")
        dysonAccount.login()
        deviceList = dysonAccount.devices()
        if len(deviceList)>0:
            Domoticz.Debug("number of devices: '"+str(len(deviceList))+"'")
        else:
            Domoticz.Debug("no devices found")
        
    def onStop(self):
        Domoticz.Debug("onStop called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("DysonPureLink plugin: onNotification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")

    def onDeviceRemoved(self):
        Domoticz.Log("DysonPureLink plugin: onDeviceRemoved called")

    def _hashed_password(self, pwd):
        """Hash password (found in manual) to a base64 encoded of its shad512 value"""
        hash = hashlib.sha512()
        hash.update(pwd.encode('utf-8'))
        return base64.b64encode(hash.digest()).decode('utf-8')

        
global _plugin
_plugin = TestPlug()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Color):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Color)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def onDeviceRemoved():
    global _plugin
    _plugin.onDeviceRemoved()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return