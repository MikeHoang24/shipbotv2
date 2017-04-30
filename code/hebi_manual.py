# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 22:16:12 2017

@author: Michu
"""

class Hebi:
    def __init__(self, fname):
        self.fname = fname

    def send(self, hebi0, hebi1, hebi2):
        f = open(self.fname, 'w')
        f.write("@ 1\n")
        f.write("s " + str(int(hebi0)) + "\n")
        f.write("e " + str(int(hebi1)) + "\n")
        f.write("h " + str(int(hebi2)))
        f.close()
        
    def terminate(self):
        f = open(self.fname, 'w')
        f.write("@ 1\n")
        f.write("STOP")
        f.close()

hebi = Hebi("hebi_info.txt")
terminate = False
while not terminate:
    val0 = raw_input("Input hebi0 value : ")
    val1 = raw_input("Input hebi1 value : ")
    val2 = raw_input("Input hebi2 value : ")
    if val0 == "c" or val1 == "c" or val2 == "c":
        terminate = True
    else:
        hebi.send(int(val0), int(val1), int(val2))