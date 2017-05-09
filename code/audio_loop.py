# -*- coding: utf-8 -*-
"""
Created on Sat May 06 14:20:14 2017

@author: Michu
"""

from pygame import mixer as mix
import time

class audioPlayer():
    def __init__(self):
        mix.init()
        time.sleep(1)
        self.q = []
        self.info = 0
        self.music = 1
        self.fname = 'audio_queue.txt'
        mix.Channel(self.info).stop()
        mix.Channel(self.music).stop()
        #open(self.fname, 'w').close()
        print("init info player")
        
    def playInfo(self, fname):
        fname = "sound/" + fname + ".wav"
        stream = mix.Sound(fname)
        mix.Channel(self.info).queue(stream)
        
    def readInfo(self):
        with open(self.fname, 'r') as f:
            contents = f.readlines()
        #print self.fname
        contents = [x.strip() for x in contents]
        res = []
        for content in contents:
            content.split()
            temp = content.split()
            res += temp
        #print res
        return res
    
    def deleteFirstStream(self):
        with open(self.fname, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(self.fname, 'w') as fout:
            fout.writelines(data[1:])
        
    def flush(self):
        mix.init()
        #print("in flush")
        while True:
            #print("in loop")
            if not mix.Channel(self.info).get_busy():
                data = self.readInfo()
                #print("channel free")
                #print len(data)
                if (len(data) > 0):
                    if data[0] == 'STOP':
                        #print("stopping")
                        self.deleteFirstStream()
                        break
                    else:
                        #print("playing " + data[0])
                        self.playInfo(data[0])
                        self.deleteFirstStream()
            #print("channel busy")
            time.sleep(0.25)
            
playa = audioPlayer()
playa.flush()
