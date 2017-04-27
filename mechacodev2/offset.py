# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 22:14:30 2017

@author: Michu
"""
import math

def offsets(x_off):
    print("Calculating offset, cv_off = " + str(x_off))
    L = 153.0
    theta1 = math.asin(x_off/L)/math.pi*180.0
    theta2 = -theta1
    up = L-L*math.cos(theta1*math.pi/180.0)
    return (up, theta1, theta2)