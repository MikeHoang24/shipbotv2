# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 22:14:30 2017

@author: Michu
"""
import math

def offset_valves(x_off, L):
    print("Calculating offset, cv_off = " + str(x_off))
    if abs(x_off) <= L:
        theta1 = math.asin(float(x_off)/L)
        theta2 = -theta1
        up = L-L*math.cos(theta1)
        return (up, theta1/math.pi*180.0, theta2/math.pi*180.0)
    else:
        print("Offset too large, just extending to maximum")
        if x_off < 0:
            return (L, -90, -180)
        else:
            return (L, 90, -180)
    
def offset_breakers(x_off, L, L2):
    print("Calculating offset, cv_off = " + str(x_off))
    if abs(x_off) <= L:
        theta1 = math.asin(float(x_off)/L)
        theta2 = -theta1
        up = L-L*math.cos(theta1)
        return (up, theta1/math.pi*180.0, theta2/math.pi*180.0)
    else:
        print("Offset too large, just extending to maximum")
        if x_off < 0:
            return (L, -90, -180)
        else:
            return (L, 90, -180)
