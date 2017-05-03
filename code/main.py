# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 19:04:19 2017

@author: Michu
"""

import devices
import station
import parse
import state
import offset
import capture
import hand
import time

drive_port = "/dev/ttyACM1"
stepper_port = "/dev/ttyACM0"
hebi_fname = "hebi_info.txt"
debug = False #set to True when debugging code
hand_input = True #set to True to turn computer vision off

if not hand_input:
    import picamera

stationD_x = 254 #distance robot needs to move from station D to station E
stationG_y = 229 #distance robot needs to move from station F to station G
station_dist = 303 #distance robot needs to move from station to a neighboring one
max_L = 153
max_L2 = max_L + 35
init_station = "A"

s = state.state(drive_port, stepper_port, hebi_fname, init_station, debug) #initialize robot state
#X-coord, Y-coord, Orientation (0/1 = Short/Long side)
st_a = station.Station("A", stationD_x + station_dist*3, 0, 1)
st_b = station.Station("B", stationD_x + station_dist*2, 0, 1)
st_c = station.Station("C", stationD_x + station_dist, 0, 1)
st_d = station.Station("D", stationD_x, 0, 1)
st_e = station.Station("E", 0, 0, 1)
st_f = station.Station("F", 0, 0, 0)
st_g = station.Station("G", 0, stationG_y, 0)
st_h = station.Station("H", 0, stationG_y + station_dist, 0)

#initialize axes (wait a second to give time for serial ports to open)
time.sleep(2)
s.init_axes()

#Rest positions
rest_y = 270
rest_z = 20
rest_hebi0 = -90
rest_hebi1 = 0
rest_hebi2 = 0

#Initial positions
init_y = 250
init_z = 10
init_hebi0 = 0
init_hebi1 = 0
init_hebi2 = 0

big_pullback = 0#10
shuttle_rotate = 100 #rotation needed to turn shuttlecock valve by 90 degrees
shuttle_pullback = 0 #angle pulled back after engaging shuttlecock valve
breaker_dist = 53 #distance between middle switch in breaker and side switch in mm
breaker_a_middle = 15
breaker_b_middle = -5
breaker_pullback = 0 #distance pulled back after flipping breaker in mm
big_cw_gap = 0#42 #gap from green marker on big valve to arm in cw direction
big_ccw_gap = 0#20 #gap from green marker on big valve to arm in ccw direction
max_offset = 153 #maximum reachable offset of the arm in mm
E_offset = 70
F_offset = -100 #-88

missions = parse.parse_mission("mission_file.txt")

print("INITIAL POSITION:") #setting robot to rest position
s.set_y(init_y)
s.set_z(init_z)
s.set_hebiall(init_hebi0, init_hebi1, init_hebi2)

raw_input("Press ENTER to start mission...")

if not hand_input:
    camera = picamera.PiCamera()

s.move_f() #Moving forward until hitting the wall (just in case)
for mission in missions:
    while (ord(mission[0]) > ord(s.c_s)):
	s.set_y(rest_y)
	s.set_z(rest_z)
	s.set_hebiall(rest_hebi0, rest_hebi1, rest_hebi2)
        if (s.c_s == "D"):
            s.move_a("245 0 1 0 0 1")
        elif (s.c_s == "E"):
            s.move_a("0 0 1 0 0 0")
        elif (s.c_s == "F"):
            s.move_r(stationG_y)
            s.move_f()
        else:
            s.move_r(station_dist)
            s.move_f()
	time.sleep(1)
        s.set_station(chr((ord(s.c_s)+1)))
    else:
        if not hand_input:
            (cv_off, cv_green, cv_ori) = capture.cv_info(camera, mission[1]) #Computer Vision
        else:
            cv_off = 0
            cv_green = hand.get_angle(ord(s.c_s)-ord("A"))
            cv_ori = hand.get_ori(ord(s.c_s)-ord("A"))
        if (s.c_s == "E"):
            cv_off = E_offset
        elif (s.c_s == "F"):
            cv_off = F_offset
        else:
            if cv_off < -max_L:
                s.move_l(cv_off)
                (cv_off, cv_green, cv_ori) = capture.cv_info(mission[1])
            elif cv_off > max_L:
                s.move_r(cv_off)
                (cv_off, cv_green, cv_ori) = capture.cv_info(mission[1])
        (up, theta1, theta2) = offset.offset_valves(cv_off, max_L)
        if (mission[1] == "V1"): #SMALL VALVE
            target_angle = int(mission[2])
            rotate = target_angle - cv_green
            s.c_d = devices.Small(cv_ori)
            s.set_hebiall(s.c_d.hebi0, s.c_d.hebi1 + theta1, s.c_d.hebi2 + theta2)
            if cv_ori == "V":
                s.set_z(s.c_d.z1 + up)
                s.set_y(s.c_d.y1)
                s.set_hebi2(s.hebi2 + rotate)
            elif cv_ori == "H":
                s.set_z(s.c_d.z0)
                s.set_y(s.c_d.y0 - up)
                s.set_z(s.c_d.z1)
                s.set_hebi2(s.hebi2 + rotate)
                s.set_z(s.c_d.z0)  
        elif (mission[1] == "V2"): #BIG VALVE
            target_angle = int(mission[2])
            rotate = target_angle - cv_green
            s.c_d = devices.Big()
            s.set_hebiall(s.c_d.hebi0, s.c_d.hebi1 + theta1, s.c_d.hebi2 + theta2 + cv_green)
            s.set_z(s.c_d.z1 + up)
            s.set_y(s.c_d.y1)
            if rotate > 0:
                s.rotate_hebi2(rotate + big_cw_gap)
                s.rotate_hebi2(-big_pullback)
            else:
                s.rotate_hebi2(rotate - big_ccw_gap)
                s.rotate_hebi2(big_pullback)
        elif (mission[1] == "A" or mission[1] == "B"): #BREAKERS
            target = mission[2]
            s.c_d = devices.Breaker(mission[1])
            if mission[1] == "A":
                breaker_middle = breaker_a_middle
            else:
                assert(mission[1] == "B")
                breaker_middle = breaker_b_middle
            if (target == "B1"):
                (up, theta1, theta2) = offset.offset_breakers(cv_off-breaker_dist+breaker_middle, max_L, max_L2)
            elif (target == "B3"):
                (up, theta1, theta2) = offset.offset_breakers(cv_off+breaker_dist+breaker_middle, max_L, max_L2)
            else:
                assert(target == "B2")
                (up, theta1, theta2) = offset.offset_breakers(cv_off+breaker_middle, max_L, max_L2)
            y_in = s.c_d.y0
            if abs(cv_off) > 59:
                y_in -= abs(cv_off)/20
            s.set_z(s.c_d.z0+up)
            s.set_hebiall(s.c_d.hebi0, s.c_d.hebi1+theta1, s.c_d.hebi2+theta2)
            #if (target == "B1" or target == "B3"):
            #    y_calibrate = s.c_d.y0 + 2
            #else:
            #    y_calibrate = s.c_d.y0
            s.set_y(y_in)
            s.set_z(s.c_d.z1+up)
            if (s.c_d.z1 > s.c_d.z0):
                s.offset_z(-breaker_pullback)
            else:
                assert(s.c_d.z1 < s.c_d.z0)
                s.offset_z(breaker_pullback)
        elif (mission[1] == "V3"): #SHUTTLECOCK
            target = int(mission[2])
            s.c_d = devices.Shuttle(cv_ori)
            if (cv_ori == "V"):
                s.set_z(s.c_d.z0 + up)
                if (target == 0):
                    s.set_hebiall(s.c_d.hebi0c, s.c_d.hebi1c + theta1, s.c_d.hebi2c + theta2)
                    s.set_y(s.c_d.y0)
                    s.rotate_hebi2(-shuttle_rotate)
                    s.rotate_hebi2(-shuttle_pullback)
                elif (target == 1):
                    s.set_hebiall(s.c_d.hebi0o, s.c_d.hebi1o + theta1, s.c_d.hebi2o + theta2)
                    s.set_y(s.c_d.y0)
                    s.rotate_hebi2(shuttle_rotate)
                    s.rotate_hebi2(shuttle_pullback)
                else:
                    print("Invalid shuttle target")
            elif (cv_ori == "H"):
                s.set_z(s.c_d.z0)
                if (target == 0):
                    s.set_hebiall(s.c_d.hebi0c, s.c_d.hebi1c + theta1, s.c_d.hebi2c + theta2)
                    s.set_y(s.c_d.y0-up)
                    s.set_z(s.c_d.z1)
                    s.rotate_hebi2(-shuttle_rotate)
                    s.rotate_hebi2(-shuttle_pullback)
                    s.set_z(s.c_d.z0)
                elif (target == 1):
                    s.set_hebiall(s.c_d.hebi0o, s.c_d.hebi1o + theta1, s.c_d.hebi2o + theta2)
                    s.set_y(s.c_d.y0-up)
                    s.set_z(s.c_d.z1)
                    s.rotate_hebi2(shuttle_rotate)
                    s.rotate_hebi2(shuttle_pullback)
                    s.set_z(s.c_d.z0)
                    
        else:
            print("Invalid device")
        print("Finished Engaging Device: " + s.c_d.name + " at station "
              + s.c_s + " with orientation " + cv_ori)
        if (s.c_d.name == "Small" or s.c_d.name == "Big"):
            print("From angle: " + str(cv_green) + " to " + mission[2] + ". Rotate by: " + str(rotate))
        print("REST POSITION:")
        s.set_y(rest_y)
        s.set_z(rest_z)
        s.set_hebiall(rest_hebi0, rest_hebi1, rest_hebi2)
        
time.sleep(1)
if not debug:
    s.hebi_terminate()
    s.drive_terminate()
    s.stepper_terminate()
