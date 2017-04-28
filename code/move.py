# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 20:40:02 2017

@author: Michu
"""

import serial

def f():
    print("Moving forward to hit wall")
    
def r(dist):
    print("Moving right " + str(dist) + " units")
    
def l(dist):
    print("Moving left " + str(dist) +  "units")
    
def u(dist):
    print("Moving up " + str(dist) + " units")
    
def a(string):
    print("All movement command: " + string)