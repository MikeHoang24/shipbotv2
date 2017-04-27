# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:07:20 2017

@author: Michu
"""

import devices
import station
import parse
import state
import offset
import capture
import hand

s = state.state()
st_a = station.Station("A", 1156, 0, 1) #X-coord, Y-coord, Orientation (0/1 = Short/Long side)
st_b = station.Station("B", 851, 0, 1)
st_c = station.Station("C", 546, 0, 1)
st_d = station.Station("D", 241, 0, 1)
st_e = station.Station("E", 0, 0, 1)
st_f = station.Station("F", 0, 0, 0)
st_g = station.Station("G", 0, 245, 0)
st_h = station.Station("H", 0, 550, 0)