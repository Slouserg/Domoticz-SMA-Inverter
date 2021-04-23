# Domoticz plugin for SMA Inverters using Modbus TCP/IP


## Tested on
- Sunny TriPower [(thanks to doopa75)](https://github.com/doopa75/SMA-Inverter-ModbusTCPIP)
- Sunny Boy 3.6

## Requirements
- Modbus TCP enabled ([check this](https://www.sma-sunny.com/en/how-to-test-the-connection-to-your-sma-inverter/))

> My installer used the following default password for the 'installer' account: `postalCode_zf` (for example `1234AB_zf`)

## Installation
```bash
cd ~/domoticz/plugins
git clone https://github.com/Slouserg/Domoticz-SMA-Inverter.git
cd Domoticz-SMA-Inverter
pip3 install -U pymodbus pymodbusTCP
systemctl restart domoticz
```

Succesfully Tested on Domoticz version: 2020.2 (build 12453)

## Thanks

Original author: doki
Inspired by MFxMF
