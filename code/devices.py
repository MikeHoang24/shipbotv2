# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 19:08:43 2017

@author: Michu
"""

class Device:
    def __init__(self, name):
        self.name = name
        self.hebi0 = -90
        self.hebi1 = 0
        self.hebi2 = -13
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
            self.y0 = 140
            self.y1 = 140
            self.z0 = 10
            self.z1 = 10
            self.hebi0 = 0
            self.hebi1 = 0
            self.hebi2 = -13
        elif (ori == "H"):
            self.y0 = 145
            self.y1 = 145
            self.z0 = 325
            self.z1 = 300
            self.hebi0 = -90
            self.hebi1 = 30
            self.hebi2 = -13
    
class Big(Device):
    def __init__(self):
        Device.__init__(self, "Big")
        self.y0 = 149
        self.y1 = 149
        self.z0 = 7
        self.z1 = 7
        self.hebi0 = 0
        self.hebi1 = 0
        self.hebi2 = -13
        
class Shuttle(Device): #0 = open, 1 = closed
    def __init__(self, ori):
        Device.__init__(self, "Shuttle")
        self.ori = ori
        if ori == "V":
            self.y0 = 140
            self.y1 = 140
            self.z0 = 7
            self.z1 = 7
            self.hebi0o = 0
            self.hebi1o = 0
            self.hebi2o = -40
            self.hebi0c = 0
            self.hebi1c = 0
            self.hebi2c = 120
        elif ori == "H":
            self.y0 = 80
            self.y1 = 80
            self.z0 = 360
            self.z1 = 330
            self.hebi0o = -90
            self.hebi1o = 0
            self.hebi2o = 40
            self.hebi0c = 0
            self.hebi1c = 0
            self.hebi2c = 200
        
class Breaker(Device):
    def __init__(self, letter):
        Device.__init__(self, "Breaker")
        self.letter = letter
        if (letter == "A"):
            self.hebi0 = 0
            self.hebi1 = 0
            self.hebi2 = 167
            self.y0 = 147
            self.y1 = 147
            self.z0 = 70
            self.z1 = 42
        elif (letter == "B"):
            self.z0 = 10
            self.z1 = 35
            self.y0 = 147
            self.y1 = 147
            self.hebi0 = 0
            self.hebi1 = 0
            self.hebi2 = 167