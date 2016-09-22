# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 17:33:04 2016

@author: amiralidolat
"""
#from pymodbus3.constants import Endian
#from pymodbus3.payload import BinaryPayloadDecoder
from pymodbus3.client.sync import ModbusTcpClient as ModbusClient    
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
client = ModbusClient('192.168.0.18', port=502)
client.connect()

rq=client.read_holding_registers(279,27)
#rq=client.read_long(1000)
print(rq.registers)
#decoder = BinaryPayloadDecoder.fromRegisters(rq.registers, endian=Endian.Little)
client.close()

