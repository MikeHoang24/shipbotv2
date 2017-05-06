# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 14:27:21 2017

@author: Michu
"""

import serial

dev = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

TIMEOUT = 2
timeout = 0
while (timeout < TIMEOUT):
	timeout += 1
	line = dev.readline()
	if len(line) > 1:
		print "Read: " + line
		break

dev.close()

open('audio_queue.txt', 'w').close()