# -*- coding: utf-8 -*-
"""
Created on Thu May 04 13:57:02 2017

@author: Michu
"""
from pygame import mixer as mix
import time

CHUNK = 1024

class audioControl():
    def __init__(self, audio_on):
        mix.init()
        self.info = 0
        self.music = 1
        self.move_i = 0
        self.move_imax = 4
        self.audio_on = audio_on
        self.fname = 'audio_queue.txt'
        open(self.fname, 'w').close()
        
    def playMusic(self, fname):
        if self.audio_on:    
            fname = "sound/" + fname + ".wav"
            stream = mix.Sound(fname)
            if not mix.Channel(self.music).get_busy:
                mix.Channel(self.music).play(stream)
        
    def queueInfo(self, streamName):
        with open(self.fname, 'a') as fin:
            fin.write(streamName + '\n')
            
    def queue_number(self, number):
        if number == 0:
            self.queueInfo("0")
        else:
            if number < 0:
                self.queueInfo("minus")
            number = abs(number)
            numberString = list(str(number))
            for digit in numberString:
                self.queueInfo(digit)
                
    def play_init(self):
        self.queueInfo("initialize")
        
    def play_terminate(self):
        self.queueInfo("terminate")
        
    def play_station(self,letter):
        self.queueInfo("station")
        self.queueInfo(letter)
    
    def play_device(self,device):
        self.queueInfo("device")
        if device == "V1":
            fname = "small"
        elif device == "V2":
            fname = "big"
        elif device == "V3":
            fname = "shuttlecock"
        elif device == "A" or device == "B":
            fname = "breaker"
        else:
            fname = "error"

        self.queueInfo(fname)
        if device == "A":
            self.queueInfo("A")
        if device == "B":
            self.queueInfo("B")    
            
    def play_valve(self, detected, target):
        self.queueInfo("angle_detected")
        self.queue_number(detected)
        self.queueInfo("degrees")
        self.queueInfo("angle_target")
        self.queue_number(target)
        self.queueInfo("degrees")
        self.queueInfo("angle_rotate")
        self.queue_number(target-detected)
        self.queueInfo("degrees")
        
    def play_breaker(self, switch):
        self.queueInfo("switch")
        self.queueInfo(switch)
        
    def play_shuttlecock(self, finalState):
        if finalState == 1:
            self.queueInfo("close")
        elif finalState == 0:
            self.queueInfo("open")
        
    def play_orientation(self, ori):
        if ori == "V":
            self.queueInfo("vertical")
        elif ori == "H":
            self.queueInfo("horizontal")
            
    def play_move(self):
        self.playMusic("move"+str(self.move_i))
        self.move_i = (self.move_i + 1)%self.move_imax
        
    def play_turn(self):
        self.playMusic("moveturn")
        
#    def old_play(self,fname):
#        
#        fname = "sound/" + fname +".wav"
#        
#        wf = wave.open(fname, 'rb')
#        
#        p = pa.PyAudio()
#        
#        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                        channels=wf.getnchannels(),
#                        rate=wf.getframerate(),
#                        output=True)
#        
#        data = wf.readframes(CHUNK)
#        
#        while data != '':
#            stream.write(data)
#            data = wf.readframes(CHUNK)
#        
#        stream.stop_stream()
#        stream.close()
#        
#        p.terminate()