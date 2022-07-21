# Basic Python Plugin Example
#
# Author: Jan-Jaap Kostelijk
#
"""
<plugin key="testPlugIn" name="test plugin" author="Jan-Jaap Kostelijk" version="2.0.0" >
    <description>
        Test plugin<br/><br/>
        just a plugin to run some simple tests<br/>
    </description>
    <params>
		<param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
		<param field="Port" label="Port" width="30px" required="true" default="1883"/>
		<param field="Mode4" label="Debug" width="75px">
            <options>
                <option label="Verbose" value="Verbose"/>
                <option label="True" value="Debug" default="true"/>
                <option label="False" value="Normal"/>
            </options>
        </param>
        <param field="Mode2" label="Refresh interval" width="75px">
            <options>
                <option label="20s" value="2"/>
                <option label="1m" value="6"/>
                <option label="5m" value="30" default="true"/>
                <option label="10m" value="60"/>
                <option label="15m" value="90"/>
            </options>
        </param>
    </params>
</plugin>
"""

#import Domoticz
import DomoticzEx as Domoticz
import json
import time
from mqtt import MqttClient

class TestPlug:
    #define class variables

    def __init__(self):
        pass

    def onStart(self):
        Domoticz.Log("onStart called")
        if Parameters['Mode4'] == 'Debug':
            Domoticz.Debugging(2)
            DumpConfigToLog()
        if Parameters['Mode4'] == 'Verbose':
            Domoticz.Debugging(1)
            DumpConfigToLog()

        #read out parameters
        self.ip_address = Parameters["Address"].strip()
        self.port_number = Parameters["Port"].strip()
        self.base_topic = "test"
        mqtt_client_id = ""
        Domoticz.Debug("base topic defined: '"+self.base_topic+"'")
        self.runCounter = int(Parameters['Mode2'])

        #create the connection
        self.mqttClient = MqttClient(self.ip_address, self.port_number, mqtt_client_id, self.onMQTTConnected, self.onMQTTDisconnected, self.onMQTTPublish, self.onMQTTSubscribed)

        if "shutter" not in Images:
            Domoticz.Image("shutter.zip").Create()

        swtype = 15
        Domoticz.Device(DeviceID="deviceURL") #use deviceURL as identifier for Domoticz.Device instance
        Domoticz.Unit(Name="label orientation", Unit=2, Type=244, Subtype=73, Switchtype=swtype, DeviceID="deviceURL").Create()
        #Domoticz.Device(Name="label orientation", Unit=3, Type=244, Subtype=73, Switchtype=swtype, DeviceID="deviceURL", Image=Images["shutter"].ID).Create()

    def onStop(self):
        Domoticz.Debug("onStop called")

    def onCommand(self, DeviceId, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand: DeviceId: '"+str(DeviceId)+"' Unit: '"+str(Unit)+"', Command: '"+str(Command)+"', Level: '"+str(Level)+"', Hue: '"+str(Hue)+"'")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")
        self.mqttClient.onConnect(Connection, Status, Description)

    def onDisconnect(self, Connection):
        self.mqttClient.onDisconnect(Connection)

    def onMessage(self, Connection, Data):
        self.mqttClient.onMessage(Connection, Data)

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("onNotification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        self.runCounter = self.runCounter - 1
        if self.runCounter <= 0:
            Domoticz.Debug("Poll unit")
            self.runCounter = int(Parameters['Mode2'])
            self.mqttClient.onHeartbeat()

    def onDeviceAdded(self, DeviceID, Unit):
        Domoticz.Debug("onDeviceAdded called for DeviceID {0} and Unit {1}".format(DeviceID, Unit))

    def onDeviceModified(self, DeviceID, Unit):
        Domoticz.Debug("onDeviceModified called for DeviceID {0} and Unit {1}".format(DeviceID, Unit))

    def onDeviceRemoved(self, DeviceID, Unit):
        Domoticz.Debug("onDeviceRemoved called for DeviceID {0} and Unit {1}".format(DeviceID, Unit))

    def onMQTTConnected(self):
        """connection to device established"""
        Domoticz.Debug("onMQTTConnected called")
        self.mqttClient.Subscribe([self.base_topic + '/#', '/#']) #subscribe to all topics on the broker

    def onMQTTDisconnected(self):
        Domoticz.Debug("onMQTTDisconnected")

    def onMQTTSubscribed(self):
        Domoticz.Debug("onMQTTSubscribed")
        
    def onMQTTPublish(self, topic, message):
        Domoticz.Debug("MQTT Publish: MQTT message incoming: " + topic + " " + str(message))

        if (topic == self.base_topic + '/testdata'):
            #receiving tes data
            Domoticz.Debug("tes data received")
            #message = json.loads(message)
            data = message['data']
            #self.UpdateDevice(3, int(data["nvalue"]), data["svalue"])
            self.UpdateDeviceEx("deviceURL", 2, int(data["nvalue"]), data["svalue"])

        if (topic == self.base_topic + '/status/connection'):
            #connection status received
            Domoticz.Debug("connection state recieved")

        if (topic == self.base_topic + '/status/software'):
            #connection status received
            Domoticz.Debug("software state recieved")
            
        if (topic == self.base_topic + '/status/summary'):
            #connection status received
            Domoticz.Debug("summary state recieved")


    def UpdateDeviceEx(self, DeviceID, Unit, nValue, sValue, BatteryLevel=255, AlwaysUpdate=False):
            
        Devices[DeviceID].Units[Unit].nValue = nValue
        Devices[DeviceID].Units[Unit].sValue = str(sValue)
        Devices[DeviceID].Units[Unit].LastLevel = int(sValue)
        Devices[DeviceID].Units[Unit].Update(Log=True)

        Domoticz.Debug("Update %s - %s: nValue %s - sValue %s - BatteryLevel %s" % (
            DeviceID,
            Unit,
            nValue,
            sValue,
            BatteryLevel
        ))

    def UpdateDevice(self, Unit, nValue, sValue, BatteryLevel=255, AlwaysUpdate=False, Name=""):
        if Unit not in Devices: return
        if Devices[Unit].nValue != nValue\
            or Devices[Unit].sValue != sValue\
            or Devices[Unit].BatteryLevel != BatteryLevel\
            or AlwaysUpdate == True:
            
            Devices[Unit].Update(nValue, str(sValue), BatteryLevel=BatteryLevel)

            Domoticz.Debug("Update %s: nValue %s - sValue %s - BatteryLevel %s" % (
                Devices[Unit].Name,
                nValue,
                sValue,
                BatteryLevel
            ))
        
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

def onCommand(DeviceId, Unit, Command, Level, Color):
    global _plugin
    _plugin.onCommand(DeviceId, Unit, Command, Level, Color)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def onDeviceAdded(DeviceID, Unit):
    global _plugin
    _plugin.onDeviceAdded(DeviceID, Unit)

def onDeviceModified(DeviceID, Unit):
    global _plugin
    _plugin.onDeviceModified(DeviceID, Unit)

def onDeviceRemoved(DeviceID, Unit):
    global _plugin
    _plugin.onDeviceRemoved(DeviceID, Unit)

    # Generic helper functions
def DumpConfigToLog():
    Domoticz.Debug("Parameters count: " + str(len(Parameters)))
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("Parameter: '" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
    return
