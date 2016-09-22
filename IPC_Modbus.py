# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 10:13:34 2016

@author: amiralidolat
"""

"""
All this to replace clear
"""
#def clear_all():
#    gl = globals().copy()
#    for var in gl:
#        if var[0] == '_': continue
#        if 'func' in str(globals()[var]): continue
#        if 'module' in str(globals()[var]): continue
#        del globals()[var]
#if __name__ == "__main__":
#    clear_all()
#    
""" Import Map for ModBus Registers """
modmap = []
import csv
with open ('/Users/amiralidolat/Documents/Python/Access Files/IPC_Modbus_Register_Map.csv', newline='') as csvfile:
    for row in csv.reader(csvfile):
        modmap.append(row)

""" Modbus Read and plot """     
import serial
import minimalmodbus
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL=True
instrument = minimalmodbus.Instrument("/dev/cu.usbserial-IP95JD6", 240)
instrument.serial.baudrate = 19200   # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_EVEN
instrument.serial.stopbits = 2
instrument.serial.timeout  = 0.5   # seconds
instrument.mode = minimalmodbus.MODE_RTU 
instrument.debug = False
instrument.handle_local_echo = False

H=[]
for i in range(1,len(modmap)):
    H.append(modmap[i][6])
import matplotlib.pyplot as plt
import numpy as np
M=[]    
j=0
while True:
    V=[]
    for i in range(1,len(modmap)):
        if modmap[i][7] == 'String(32)':
            V.append(instrument.read_string(int(modmap[i][1]),16))
        elif modmap[i][7] == 'String(16)':
            V.append(instrument.read_string(int(modmap[i][1]),8))
            
        elif modmap[i][7] == 'uint16' or modmap[i][7] == 'uint16x':
            V.append(instrument.read_register(int(modmap[i][1])))
            
        elif modmap[i][7] == 'uint32' or modmap[i][7] == 'uint32x':
            V.append(instrument.read_long(int(modmap[i][1])))
            
        elif modmap[i][7] == 'int16' or modmap[i][7] == 'int16x':
            V.append(instrument.read_register(int(modmap[i][1])))
            if int(V[i-1]) >= 32767:
                V[i-1]=int(V[i-1])-32768
                
        elif modmap[i][7] == 'int32' or modmap[i][7] == 'int32x':
            V.append(instrument.read_long(int(modmap[i][1])))
            if int(V[i-1]) >= 2147483647:
                V[i-1]=int(V[i-1])-2147483648
    M.append(V)
    del V 
    if j==0:
        M.insert(0,H)
    print('Number of scans completed:')
    print(j+1)
    if j>1:
        t=np.arange(0,j,1)
        V_aux=M[0:][130]
        plt.plot(t,V_aux,'r--')
        plt.ylabel('Voltage')
        plt.show()
    j=j+1
    if j>=100:
        break

