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
<plugin key="SMA" name="Domoticz-SMA-Inverter" version="0.8.0" author="Want100Cookies">
    <params>
        <param field="Address" label="Your SMA IP Address" width="200px" required="true" default="10.10.10.7"/>
        <param field="Port" label="Port" width="40px" required="true" default="502"/>
        <param field="Mode1" label="Device ID" width="40px" required="true" default="3" />
        <param field="Mode2" label="Reading Interval sec." width="40px" required="true" default="5" />
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
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
        Domoticz.Device(Name="Solar Production", Unit=1, Type=243, Subtype=33, SwitchType=4, Used=0).Create()
    if 2 not in Devices:
        Domoticz.Device(Name="DC Power", Unit=2, TypeName="Usage", Used=0).Create()
    if 3 not in Devices:
        Domoticz.Device(Name="AC Power", Unit=3, TypeName="Usage", Used=0).Create()
    if 4 not in Devices:
        Domoticz.Device(Name="Temperature", Unit=4, TypeName="Temperature", Used=0).Create()

    Domoticz.Heartbeat(Parameters["Mode2"])

def onHeartbeat():
    TotalYieldAddress = 30529
    DCPowerAddress = 30773
    ACPowerAddress = 30775
    TemperatureAddress = 30953

    try:
        client = ModbusClient(host=Parameters["Address"], port=Parameters["Port"], unit_id=Parameters["Mode1"], auto_open=True, auto_close=True)
        TotalYieldRead = client.read_holding_registers(TotalYieldAddress, 2)
        DCPowerRead = client.read_holding_registers(DCPowerAddress, 2)
        ACPowerRead = client.read_holding_registers(ACPowerAddress, 2)
        TemperatureRead = client.read_holding_registers(TemperatureAddress, 2)
        
    except:
        Domoticz.Log("Connection problem")
        return

    TotalYieldValue = BinaryPayloadDecoder.fromRegisters(TotalYieldRead, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_uint()
    DCPowerValue = BinaryPayloadDecoder.fromRegisters(DCPowerRead, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_uint()
    ACPowerValue = BinaryPayloadDecoder.fromRegisters(ACPowerRead, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_uint()
    TemperatureValue = BinaryPayloadDecoder.fromRegisters(TemperatureRead, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_uint()

    if Parameters["Mode6"] == 'Debug':
        Domoticz.Log(f'TotalYield\t{str(TotalYieldValue)}\DCPower\t{str(DCPowerValue)}\tACPower\t{str(ACPowerValue)}\tTemperature\t{str(TemperatureValue)}')

    if DCPowerValue == 2147483648:
        DCPowerValue = 0
    
    if ACPowerValue == 2147483648:
        ACPowerValue = 0

    if TemperatureValue == 2147483648:
        TemperatureValue = 0
    
    Devices[1].Update(0, f'{str(TotalYieldValue)};{str(ACPowerValue)}')
    Devices[2].Update(0, str(DCPowerValue))
    Devices[3].Update(0, str(ACPowerValue))
    Devices[4].Update(0, str(TemperatureValue))