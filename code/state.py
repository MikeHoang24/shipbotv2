# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:16:14 2017

@author: Michu
"""
import devices
from ard_control import Drive
from ard_control import Stepper
from hebi_control import Hebi

class state:
    def __init__(self, drive_port, stepper_port, hebifname, debug):
        self.c_s = "A"
        self.c_d = devices.Dummy()
        self.y = 270
        self.z = 10
        self.hebi0 = 0
        self.hebi1 = 0
        self.hebi2 = -13
        if not debug:
            self.drive = Drive(drive_port)
            self.stepper = Stepper(stepper_port)
            self.hebi = Hebi(hebifname)
        self.debug = debug
        
    def init_axes(self):
        if not self.debug:
            self.stepper.initialize()
            
    def set_hebiall(self, val_0, val_1, val_2):
        if not self.debug:
            self.hebi.send(val_0, val_1, val_2)
        print("Set all Hebis to " + str(val_0) + ", " + str(val_1) + ", " + str(val_2))
        self.hebi0 = val_0
        self.hebi1 = val_1
        self.hebi2 = val_2
        
    def set_hebi0(self, val):
        if not self.debug:
            self.hebi.send(val, self.hebi1, self.hebi2)
        print("Set hebi0 to " + str(val))
        self.hebi0 = val

    def set_hebi1(self, val):
        if not self.debug:
            self.hebi.send(self.hebi0, val, self.hebi2)
        print("Set hebi1 to " + str(val))
        self.hebi1 = val

    def set_hebi2(self, val):
        if not self.debug:
            self.hebi.send(self.hebi0, self.hebi1, val)
        print("Set hebi2 to " + str(val))
        self.hebi2 = val
        
    def rotate_hebi0(self, val):
        self.set_hebi0(self.hebi0 + val)

    def rotate_hebi1(self, val):
        self.set_hebi1(self.hebi1 + val)

    def rotate_hebi2(self, val):
        self.set_hebi2(self.hebi2 + val)

    def set_y(self, val):
        if not self.debug:
            self.stepper.send_ya(val)
        print("Set Y axis to " + str(val))
        self.y = val

    def set_z(self, val):
        if not self.debug:
            self.stepper.send_za(val)
        print("Set Z axis to " + str(val))
        self.z = val
        
    def offset_y(self, val):
        self.set_y(self.y + val)

    def offset_z(self, val):
        self.set_z(self.z + val)
        
    def move_r(self, val):
        if not self.debug:
            self.drive.send_r(val)
        print("Moving to the right by " + str(val) + " mm")
        
    def move_l(self, val):
        if not self.debug:
            self.drive.send_l(val)
        print("Moving to the left by " + str(val) + " mm")
        
    def move_u(self, val):
        if not self.debug:
            self.drive.send_u(val)
        print("Moving up by " + str(val) + " mm")
        
    def move_f(self):
        if not self.debug:
            self.drive.send_f()
        print("Moving forward until hitting wall")
        
    def move_a(self, val):
        if not self.debug:
            self.drive.send_a(val)
        print("Moving all command: " + val)
        
    def set_station(self, val):
        print("Robot has moved to station " + val)
        self.c_s = val
    
    def set_device(self, val):
        print("Robot in front of device: " + val)
        self.c_d = val
        
    def hebi_terminate(self):
        self.hebi.terminate()
        
    def stepper_terminate(self):
        self.stepper.terminate()
        
    def drive_terminate(self):
        self.drive.terminate()
