# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:30:46 2017

@author: Michu
"""

class Hebi:
    def __init__(self, fname):
        self.fname = fname

    def send(self, hebi0, hebi1, hebi2):
        f = open(self.fname, 'w')
        f.write("@ 1\n")
        f.write("s " + str(hebi0) + "\n")
        f.write("e " + str(hebi1) + "\n")
        f.write("h " + str(hebi2))
        f.close()
        
    def terminate(self):
        f = open(self.fname, 'w')
        f.write("@ 1\n")
        f.write("STOP")
        f.close()