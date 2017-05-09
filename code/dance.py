# -*- coding: utf-8 -*-
"""
Created on Tue May 09 16:12:06 2017

@author: Michu
"""

from hebi_control import Hebi
import time
import audio

hebi_fname = "hebi_info.txt"

hebi = Hebi(hebi_fname)

audioControl = audio.audioControl(True)

audioControl.dance()

time.sleep(7)

count = 0
while count < 10:
    #hebi.send(0, 0, 0)
    time.sleep(1)
    #hebi.send(-90, 0, 0)
    time.sleep(1)
    count += 1
    
#hebi.terminate()