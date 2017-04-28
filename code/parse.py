# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 20:19:24 2017

@author: Michu
"""

#def parse_mission(txtfile):
#    return [["A", "V1", "90"], ["B", "V3", "1"], ["D", "A", "B2"], ["F", "B", "B1"], ["F", "B", "B2"], ["F", "B", "B3"], ["H", "B", "B3"]]
    
def parse_mission(fileName):
    f = open(fileName, 'r')
    fData = f.read()
    f.close()

    # Split the text at commas
    stationList = fData.split(',')

    # Ignore Target Time
    stationList = stationList[:-1]
    instrList = []
    
    # Split station string into station, device and endVal strings
    for i,station in enumerate(stationList) :
        # Extract Station Letter
        station = station.strip();
        instrList +=  [[station[0], '', '']];

        # Split Device and end position
        station = station[1:]
        [instrList[i][1], instrList[i][2]] = station.split(' ');

        # Remove remaining Spaces
        instrList[i][1] = instrList[i][1].strip();
        instrList[i][2] = instrList[i][2].strip();

        
    return instrList