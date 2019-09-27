# Basic Python Plugin Example
#
# Author: Jan-Jaap Kostelijk
#
"""
<plugin key="tetsPlugIn" name="test plugin" author="Jan-Jaap Kostelijk" version="1.2.0" >
    <description>
        Test plugin<br/><br/>
        just a plugin to run some simple tests<br/>
        now setup to test Dyson cloud account connection
    </description>
    <params>
		<param field="Address" label="IP Address" width="200px" required="true" default="192.168.86.23"/>
		<param field="Port" label="Port" width="30px" required="true" default="1883"/>
		<param field="Mode1" label="Dyson type (Pure Cool only at this moment)">
            <options>
                <option label="455" value="455"/>
                <option label="465" value="465"/>
                <option label="469" value="469"/>
                <option label="475" value="475" default="true"/>
                <option label="527" value="527"/>
            </options>
        </param>
		<param field="Username" label="Dyson Serial No." required="true"/>
		<param field="Password" label="Dyson Password (see machine)" required="true" password="true"/>
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
import json
import time
import base64, hashlib
from mqtt import MqttClient
from dyson import DysonAccount

class TestPlug:
    #define class variables
    cloudDevice = None

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
        self.ip_address = Parameters["Address"].strip()
        self.port_number = Parameters["Port"].strip()
        #self.serial_number = Parameters['Username']
        #self.device_type = Parameters['Mode1']
        self.password = self._hashed_password(Parameters['Password'])
        
        #create a Dyson account
        Domoticz.Debug("=== start making connection to Dyson account ===")
        dysonAccount = DysonAccount(Parameters['Mode5'],Parameters['Mode3'],"NL")
        dysonAccount.login()
        deviceList = dysonAccount.devices()
        if len(deviceList)>0:
            Domoticz.Debug("number of devices: '"+str(len(deviceList))+"'")
        else:
            Domoticz.Debug("no devices found")

        if len(deviceList)==1:
            self.cloudDevice=deviceList[0]

            Domoticz.Debug("local device pwd:      '"+self.password+"'")
            Domoticz.Debug("cloud device pwd:      '"+self.cloudDevice.credentials+"'")
            Parameters['Username'] = self.cloudDevice.serial #take username from account
            
            Parameters['Password'] = self.cloudDevice.credentials #self.password #override the default password with the hased variant
            self.base_topic = "{0}/{1}".format(self.cloudDevice.product_type, self.cloudDevice.serial)
            mqtt_client_id = ""
            Domoticz.Debug("base topic defined: '"+self.base_topic+"'")

            #create the connection
            self.mqttClient = MqttClient(self.ip_address, self.port_number, mqtt_client_id, self.onMQTTConnected, self.onMQTTDisconnected, self.onMQTTPublish, self.onMQTTSubscribed)

        
    def onStop(self):
        Domoticz.Debug("onStop called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")
        self.mqttClient.onConnect(Connection, Status, Description)

    def onDisconnect(self, Connection):
        self.mqttClient.onDisconnect(Connection)

    def onMessage(self, Connection, Data):
        self.mqttClient.onMessage(Connection, Data)

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("DysonPureLink plugin: onNotification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")

    def onDeviceRemoved(self):
        Domoticz.Log("DysonPureLink plugin: onDeviceRemoved called")

    def onMQTTConnected(self):
        """connection to device established"""
        Domoticz.Debug("onMQTTConnected called")
        self.mqttClient.Subscribe([self.base_topic + '/#']) #subscribe to topics on the machine
        payload = self.cloudDevice.request_state()
        topic = '{0}/{1}/command'.format(self.cloudDevice.product_type, self.cloudDevice.serial)
        self.mqttClient.Publish(topic, payload) #ask for update of current status

    def onMQTTDisconnected(self):
        Domoticz.Debug("onMQTTDisconnected")

    def onMQTTSubscribed(self):
        Domoticz.Debug("onMQTTSubscribed")
        
    def onMQTTPublish(self, topic, message):
        Domoticz.Debug("MQTT Publish: MQTT message incoming: " + topic + " " + str(message))

        if (topic == self.base_topic + '/status/current'):
            #update of the machine's status
            Domoticz.Debug("machine state recieved")

        if (topic == self.base_topic + '/status/connection'):
            #connection status received
            Domoticz.Debug("connection state recieved")

        if (topic == self.base_topic + '/status/software'):
            #connection status received
            Domoticz.Debug("software state recieved")
            
        if (topic == self.base_topic + '/status/summary'):
            #connection status received
            Domoticz.Debug("summary state recieved")

    def _hashed_password(self, pwd):
        """Hash password (found in manual) to a base64 encoded of its sha512 value"""
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
    Domoticz.Debug("Parameter count: " + str(len(Parameters)))
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "Parameter '" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return