# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 19:12:00 2017

@author: Michu
"""
import devices

class Station:
    def __init__(self, name, x, y, ori):
        self.name = name
        self.x = x
        self.y = y
        self.ori = ori
        self.devices = devices.Dummy()
        
    def set_x(self, x):
        self.x = x
        
    def set_y(self, y):
        self.y = y
        
    def set_device(self, device):
        self.device = device
        
    def set_ori(self, ori):
        self.ori = ori