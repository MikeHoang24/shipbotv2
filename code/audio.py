# -*- coding: utf-8 -*-
"""
Created on Thu May 04 13:57:02 2017

@author: Michu
"""

from pygame import mixer as mix
import time

CHUNK = 1024

class audioControl():
    def __init__(self):
        mix.init()
	self.maxChannels = mix.get_num_channels()
        self.info = 0
        self.music = 1
        
    def play(self, fname):
        fname = "sound/" + fname + ".wav"
        mix.Channel(self.info).queue(mix.Sound(fname))
        
    def playMusic(self, fname):
        fname = "sound/" + fname + ".wav"
        mix.Channel(self.music).queue(mix.Sound(fname))
        
    def play_station(self,letter):
        self.play("station")
        self.play(letter)
        
    def lol(self):
        print("heh")
    
    def play_device(self,device):
        #self.play("device")
#        mix.music.queue('sound/'+device+'.wav')
#        mix.music.queue('sound/station.wav')
#        mix.music.queue('sound/'+device+'.wav')
#        mix.music.queue('sound/C.wav')
        self.play("A")
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

        self.play("move2")
        time.sleep(5)
        if device == "A":
            self.play("E")
        if device == "B":
            self.play("B")
        #if True:
        #    self.play("F")
 	self.play("move0")   

    def old_play(self,fname):
        
        fname = "sound/" + fname +".wav"
        
        wf = wave.open(fname, 'rb')
        
        p = pa.PyAudio()
        
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        data = wf.readframes(CHUNK)
        
        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)
        
        stream.stop_stream()
        stream.close()
        
        p.terminate()

#play("station")
#play("device")
audiocontrol = audioControl()
audiocontrol.play_device("A")
audiocontrol.play("breaker")
audiocontrol.play("A")
mix.Channel(0).play(mix.Sound("sound/move0.wav"))
