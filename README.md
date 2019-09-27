# domoticz-test-plugin

## Prerequisites
The following Python modules installed
```
sudo apt-get update
sudo apt-get install python3-requests
sudo pip3 install crypto
```

## Installation

1. Clone repository into your domoticz plugins folder
```
cd domoticz/plugins
git clone https://github.com/JanJaapKo/domoticz-test-plugin
```
to update:
```
cd domoticz/plugins/DysonPureLink
git pull https://github.com/JanJaapKo/domoticz-test-plugin
```
2. Restart domoticz
3. Go to "Hardware" page and add new item with type "test plugin"

## Configuration
Set the following parameters: <br>
IP Adress: adres where your machine is connected to <br>
Port number: 1883 <br>
Dyson password: the password used in the app <br>
email adress: the adress used to create the account <br>
log level: use verbose preferably <br>

You can ommit the parameters: <br>
Dyson Password (see machine): <br>
Dyson Serial No.: <br>
Dyson type (Pure Cool only at this moment): <br>
