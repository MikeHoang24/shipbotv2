# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 23:24:52 2017

@author: Michu
"""

import serial
import time

drive_port = "COM6"
stepper_port = "COM3"

ser = serial.Serial(drive_port, 9600, timeout=5)
time.sleep(1)
ser.write("f\n")
line = ser.readline()
while not ("DONE" in line):
    line = ser.readline()
print(line)
print ("drive test complete")
ser.close()



ser2 = serial.Serial(stepper_port, 9600, timeout=5)
time.sleep(2)
ser2.write("zi")
ser2.flush()
line = ser2.readline()
print(line)
print("stepper test complete")
ser2.close()