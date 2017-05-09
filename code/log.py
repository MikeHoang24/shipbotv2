# -*- coding: utf-8 -*-
"""
Created on Tue May 09 14:46:38 2017

@author: Michu
"""

import time
from datetime import datetime,tzinfo,timedelta

class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
            return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
         return self.name

EST = Zone(-4,False,'EST')

class log():
    def __init__(self):
        self.fname = 'mission_log.txt'
        open(self.fname, 'w').close()
        self.init_time = time.time()
        
    def starttime(self):
        self.init_time = time.time()
        
    def timestamp(self):
        return datetime.now(EST).strftime('%m/%d/%Y %H:%M:%S ')
    
    def timefromstart(self):
        curr = time.time() - self.init_time
        curr = int(curr)
        if curr > 59:
            mins = curr/60
            secs = curr%60
            return '[' + str(mins) + ' min ' + str(secs) + ' sec]'
        return '[' + str(curr) + ' sec]'
    
    def terminate(self):
        with open(self.fname, 'a') as fin:
            fin.write('Mission accomplished in ' + self.timefromstart() + '\n')
    
    def write(self, message):
        with open(self.fname, 'a') as fin:
            fin.write(self.timestamp() + self.timefromstart() + ' >>> ' + message + '\n')
            
    def manipulation(self, station, device):
        name = "valve"
        if device == "A":
            name = "breaker 'A'"
        elif device == "B":
            name = "breaker 'B'"
        elif device == "V1":
            name = "blue valve"
        elif device == "V2":
            name = "orange valve"
        elif device == "V3":
            name = "shuttlecock valve"
        self.write("Manipulating " + name + " at station " + station)

    def newline(self):
        with open(self.fname, 'a') as fin:
            fin.write('\n')