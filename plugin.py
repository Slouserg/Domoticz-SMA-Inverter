#!/usr/bin/env python
"""
SMA Solar Inverter
Author: Want100Cookies
Requirements:
    1. SMA Sunny Tripower or Sunny Boy with Modbus TCP enabled.
    2. python 3.x
    3. pip3 install -U pymodbus pymodbusTCP

"""
"""
<plugin key="SMA" name="SMA Solar Inverter (modbus TCP/IP)" version="0.8.0" author="Want100Cookies">
    <params>
        <param field="Address" label="Your SMA IP Address" width="200px" required="true" default="10.10.10.7"/>
        <param field="Port" label="Port" width="40px" required="true" default="502"/>
        <param field="Mode1" label="Device ID" width="40px" required="true" default="3" />
        <param field="Mode2" label="Reading Interval sec." width="40px" required="true" default="5" />
    </params>
</plugin>
"""

from pyModbusTCP.client import ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import Domoticz

def onStart():
    Domoticz.Log("Domoticz SMA Inverter Modbus plugin start")

    if 1 not in Devices:
        Domoticz.Device(Name="Solar Yield", Unit=1, TypeName="kWh", Used=0).Create()
    if 2 not in Devices:
        Domoticz.Device(Name="DC Power A", Unit=2, TypeName="Usage", Used=0).Create()
    if 3 not in Devices:
        Domoticz.Device(Name="DC Power B", Unit=3, TypeName="Usage", Used=0).Create()
    if 4 not in Devices:
        Domoticz.Device(Name="AC Power", Unit=4, TypeName="Usage", Used=0).Create()
    if 5 not in Devices:
        Domoticz.Device(Name="Temperature", Unit=5, TypeName="Temperature", Used=0).Create()

    global client
    client = ModbusClient(host=Parameters["Address"], port=Parameters["Port"], unit_id=Parameters["Mode1"])
    client.open()

    Domoticz.Heartbeat(int(Parameters["Mode2"]))

def onHeartbeat():
    TotalYieldAddress = 30529
    DCPowerAAddress = 30773
    DCPowerBAddress = 30961
    ACPowerAddress = 30775
    TemperatureAddress = 30953

    if not client.is_open():
        Domoticz.Log("Not connected. Reconnecting...")
        client.open()
        return
    
    TotalYieldRead = client.read_holding_registers(TotalYieldAddress, 2)
    DCPowerARead = client.read_holding_registers(DCPowerAAddress, 2)
    DCPowerBRead = client.read_holding_registers(DCPowerBAddress, 2)
    ACPowerRead = client.read_holding_registers(ACPowerAddress, 2)
    TemperatureRead = client.read_holding_registers(TemperatureAddress, 2)

    TotalYieldValue = BinaryPayloadDecoder.fromRegisters(TotalYieldRead, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_uint()
    DCPowerAValue = BinaryPayloadDecoder.fromRegisters(DCPowerARead, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_uint()
    DCPowerBValue = BinaryPayloadDecoder.fromRegisters(DCPowerBRead, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_uint()
    ACPowerValue = BinaryPayloadDecoder.fromRegisters(ACPowerRead, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_uint()
    TemperatureValue = BinaryPayloadDecoder.fromRegisters(TemperatureRead, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_uint()

    if DCPowerAValue == 2147483648:
        DCPowerAValue = 0
    
    if DCPowerBValue == 2147483648:
        DCPowerBValue = 0
    
    if ACPowerValue == 2147483648:
        ACPowerValue = 0

    if TemperatureValue == 2147483648:
        TemperatureValue = 0
    
    Devices[1].Update(0, str(TotalYieldValue) + ";" + str(ACPowerValue))
    Devices[2].Update(0, str(DCPowerAValue))
    Devices[3].Update(0, str(DCPowerBValue))
    Devices[4].Update(0, str(ACPowerValue))
    Devices[5].Update(0, str(TemperatureValue / 10))