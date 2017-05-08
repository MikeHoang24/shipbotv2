# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:19:04 2017

@author: Michu
"""
import serial
import time

drive_timeout = 1500
stepper_timeout = 15

class Drive():
    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port, 9600, timeout=1)
        self.receive_timeout = drive_timeout
        
    def send_a(self, val):
        self.serial.write("a ")
        self.serial.write(val+"\n")
        response = self.receive()
        return response
        
    def send_f(self):
        self.serial.write("f\n")
        response = self.receive()
        return response
        
    def send_u(self, val):
        self.serial.write("u ")
        self.serial.write(str(int(val))+"\n")
        response = self.receive()
        return response
        
    def send_l(self, val):
        self.serial.write("l ")
        self.serial.write(str(int(val))+"\n")
        response = self.receive()
        return response
        
    def send_r(self, val):
        self.serial.write("r ")
        self.serial.write(str(int(val))+"\n")
        response = self.receive()
        return response
        
    def receive(self):
        timeout = 0
        while (timeout < self.receive_timeout):
            line = self.serial.readline()
            timeout += 1
            #print("drive: " + str(timeout))
            if "DONE" in line:
                return 1
        print("Drive timed out")
        return 0
    
    def terminate(self):
        self.serial.close()
        
class Stepper():
    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port, 9600, timeout=1)
        self.receive_timeout = stepper_timeout
        
    def initialize(self):
        self.serial.write("yi")
        self.serial.flush()
        response = self.receive()
        time.sleep(1)
        self.serial.write("zi")
        self.serial.flush()
        response = self.receive()
    
    def send_ya(self, val):
        self.serial.write("ya")
        self.serial.write(str(int(val)))
        self.serial.flush()
        response = self.receive()
        
    def send_za(self, val):
        self.serial.write("za")
        self.serial.write(str(int(val)))
        self.serial.flush()
        response = self.receive()
        
    def send_yr(self, val):
        self.serial.write("yr")
        self.serial.write(str(int(val)))
        self.serial.flush()
        response = self.receive()
        
    def send_zr(self, val):
        self.serial.write("zr")
        self.serial.write(str(int(val)))
        self.serial.flush()
        response = self.receive()
        
    def receive(self):
        timeout = 0
        while (timeout < self.receive_timeout):
            line = self.serial.readline()
            timeout += 1
            #print("stepper:" + str(timeout))
            if len(line) > 0:
                return 1
        print("Stepper timed out")
        return 0
    
    def terminate(self):
        self.serial.close()
