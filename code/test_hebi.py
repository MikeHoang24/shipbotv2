# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 17:24:25 2017

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
    val = raw_input("Input hebi2 value (or 'c' to escape): ")
    if val == "C" or val == "c":
        terminate = True
    else:
        hebi.send(0, 0, int(val))