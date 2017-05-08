# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 19:08:43 2017

@author: Michu
"""

hebi2_zero = 45

class Device:
    def __init__(self, name):
        self.name = name
        self.hebi0 = -90
        self.hebi1 = 0
        self.hebi2 = hebi2_zero
        self.y0 = 170
        self.z0 = 10
        self.y1 = 170
        self.z1 = 10
        self.ori = "V"
        
#    def set_name(self, name):
#        self.name = name
#    
#    def set_hebi0(self, val):
#        self.hebi0 = val
#
#    def set_hebi1(self, val):
#        self.hebi1 = val
#
#    def set_hebi2(self, val):
#        self.hebi2 = val
#
#    def set_y0(self, val):
#        self.y0 = val
#
#    def set_y1(self, val):
#        self.y1 = val
#
#    def set_z0(self, val):
#        self.z0 = val
#
#    def set_ori(self, val):
#        self.ori = val
        
class Dummy(Device):
    def __init__(self):
        Device.__init__(self, "Dummy")
        
class Small(Device):
    def __init__(self, ori):
        Device.__init__(self, "Small")
        self.ori = ori
        if (ori == "V"):
            self.y0 = 150
            self.y1 = 150
            self.z0 = 10
            self.z1 = 10
            self.hebi0 = 0
            self.hebi1 = 0
            self.hebi2 = hebi2_zero+180
        elif (ori == "H"):
            self.y0 = 164
            self.y1 = 164
            self.z0 = 335
            self.z1 = 295
            self.hebi0 = -90
            self.hebi1 = 0
            self.hebi2 = hebi2_zero+180
    
class Big(Device):
    def __init__(self):
        Device.__init__(self, "Big")
        self.y0 = 135
        self.y1 = 135
        self.z0 = 12
        self.z1 = 12
        self.hebi0 = 0
        self.hebi1 = 0
        self.hebi2 = hebi2_zero
        
class Shuttle(Device): #0 = open, 1 = closed
    def __init__(self, ori):
        Device.__init__(self, "Shuttle")
        self.ori = ori
        if ori == "V":
            #self.y0 = 145
            #self.y1 = 145
            self.y0 = 130
            self.y1 = 130
            self.z0 = 7
            self.z1 = 7
            self.hebi0o = 0
            self.hebi1o = 0
            self.hebi2o = hebi2_zero
            self.hebi0c = 0
            self.hebi1c = 0
            self.hebi2c = hebi2_zero + 90
        elif ori == "H":
            self.y0 = 91
            self.y1 = 91
            self.z0 = 340
            self.z1 = 300
            self.hebi0o = -90
            self.hebi1o = 0
            self.hebi2o = hebi2_zero + 90
            self.hebi0c = -90
            self.hebi1c = 0
            self.hebi2c = hebi2_zero + 180
        
class Breaker(Device):
    def __init__(self, letter):
        Device.__init__(self, "Breaker")
        self.letter = letter
        if (letter == "A"):
            self.hebi0 = 0
            self.hebi1 = 0
            self.hebi2 = hebi2_zero + 180
            #self.y0 = 144
            #self.y1 = 144
            self.y0 = 118
            self.y1 = 118
            #self.z0 = 5
            #self.z1 = 42
            self.z0 = 30
            self.z1 = 7
        elif (letter == "B"):
            self.z0 = 7
            self.z1 = 25
            self.y0 = 122
            self.y1 = 122
            self.hebi0 = 0
            self.hebi1 = 0
            self.hebi2 = hebi2_zero + 180
