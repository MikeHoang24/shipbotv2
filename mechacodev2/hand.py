# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 21:53:10 2017

@author: Michu
"""

def get_angle(index):
    fname = 'valve_angles.txt'
    with open(fname, 'r') as f:
        contents = f.readlines()
    contents = [x.strip() for x in contents]
    res = []
    for content in contents:
        content.split()
        temp = content.split()
        res += temp
    if ((index*2+1 > len(res)) or (index*2+1 < 0)):
        print("Not enough hand inputs")
        return 0
    else:
        return int(res[index*2+1])
        
def get_ori(index):
    fname = 'ori_info.txt'
    with open(fname, 'r') as f:
        contents = f.readlines()
    contents = [x.strip() for x in contents]
    res = []
    for content in contents:
        content.split()
        temp = content.split()
        res += temp
    if ((index*2+1 > len(res)) or (index*2+1 < 0)):
        print("Not enough hand inputs")
        return 0
    else:
        return res[index*2+1]