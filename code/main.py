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
import audio
import log
import hand
import time

drive_port = "/dev/ttyACM1"
stepper_port = "/dev/ttyACM0"
hebi_fname = "hebi_info.txt"
debug = False #set to True when debugging code
hand_input = False #set to True to turn computer vision off
corner_adjust = False
audio_on = True
cv_dict = ["V1","V2","V3","A","B"]

if not hand_input:
    import CVController as cvcontrol
    cvc = cvcontrol.CVController()

stationD_x = 254 #distance robot needs to move from station D to station E
stationG_y = 229 #distance robot needs to move from station F to station G
station_dist = 303 #distance robot needs to move from station to a neighboring one
max_L = 153
max_L2 = max_L + 35
init_station = "A"

shuttle_rotate = 110 #rotation needed to turn shuttlecock valve by 90 degrees
breaker_dist = 55 #distance between middle switch in breaker and side switch in mm
b_a_m = 19
b_b_m = -5
if hand_input:
    breaker_a_middle = b_a_m
    breaker_b_middle = b_b_m
else:
    breaker_a_middle = 0
    breaker_b_middle = 0
max_offset = 153 #maximum reachable offset of the arm in mm
E_offset = 70
F_offset = -87 #-88
slip_big = 1.10
slip_small = 1.15
max_angle_diff = 30
max_feedback = 2

audioControl = audio.audioControl(audio_on)

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
log = log.log()
log.write('Initializing robot...')
audioControl.play_init()
s.init_axes()

#Rest positions
rest_y = 270
rest_z = 20
rest_hebi0 = -90
rest_hebi1 = 0
rest_hebi2 = 0

#Initial positions
init_y = 270
init_z = 10
init_hebi0 = -90
init_hebi1 = 0
init_hebi2 = 0

missions = parse.parse_mission("mission_file.txt")

print("INITIAL POSITION:") #setting robot to rest position

s.set_y(init_y)
s.set_z(init_z)
s.set_hebiall(init_hebi0, init_hebi1, init_hebi2)

log.starttime()
log.write('All subsystems are ready.')
audioControl.play_ready()

raw_input("Press ENTER to start mission...")
log.starttime()
log.write('File received and mission started.')
log.newline()

def rotate_calc(target, current):
    v1 = target - current
    if v1 > 180:
        return v1-360
    elif v1 < -180:
        return v1+360
    else:
        return v1

music_on = True
s.move_f() #Moving forward until hitting the wall (just in case)
for mission in missions:
    while (ord(mission[0]) > ord(s.c_s)):
        s.set_y(rest_y)
        s.set_z(rest_z)
        s.set_hebiall(rest_hebi0, rest_hebi1, rest_hebi2)
        log.write('Robot moving to station ' + chr((ord(s.c_s)+1)))
        if (s.c_s == "D"):
            if music_on:
                audioControl.play_move()
            s.move_a("245 0 1 0 0 1")
        elif (s.c_s == "E"):
            if music_on:
                audioControl.play_turn("long")
            else:
                audioControl.play_turn("short")
            s.move_a("0 0 1 0 0 0")
        elif (s.c_s == "F"):
            if music_on:
                audioControl.play_move()
            s.move_r(stationG_y)
            s.move_f()
        else:
            if music_on:
                audioControl.play_move()
            s.move_r(station_dist)
            s.move_f()
        time.sleep(1)
        s.set_station(chr((ord(s.c_s)+1)))
    else:
        audioControl.play_station(mission[0])
        audioControl.play_device(mission[1])
        log.manipulation(mission[0], mission[1])
        if ((not hand_input) and (mission[1] in cv_dict)):
            log.write('Computer vision initiated...')
            (cv_off, cv_green, cv_ori) = cvc.processCommand(mission[1]) #Computer Vision
            #cv_ori = hand.get_ori(ord(s.c_s)-ord("A")) #comment out to use orientation
            #cv_off = 0 #comment out to get offset
        else:
            cv_off = 0
            cv_green = hand.get_angle(ord(s.c_s)-ord("A"))
            cv_ori = hand.get_ori(ord(s.c_s)-ord("A"))
        if ((s.c_s == "E") and corner_adjust):
            cv_off = E_offset
            breaker_a_middle = b_a_m
            breaker_b_middle = b_b_m
        elif ((s.c_s == "F") and corner_adjust):
            cv_off = F_offset
            breaker_a_middle = b_a_m
            breaker_b_middle = b_b_m
        else:
            if not hand_input:
                breaker_a_middle = 0
                breaker_b_middle = 0
            if cv_off < -max_L:
                s.move_l(cv_off)
                (cv_off, cv_green, cv_ori) = cvc.processCommand(mission[1])
            elif cv_off > max_L:
                s.move_r(cv_off)
                (cv_off, cv_green, cv_ori) = cvc.processCommand(mission[1])
        (up, theta1, theta2) = offset.offset_valves(cv_off, max_L)
        
        #SMALL VALVE
        if (mission[1] == "V1"): 
            count = 0
            target_angle = int(mission[2])
            audioControl.play_orientation(cv_ori)
            audioControl.play_valve_target(target_angle)
            while (((abs(rotate_calc(target_angle, cv_green)) > max_angle_diff) and count <= max_feedback) or (count == 0)):
                if count != 0:
                    log.write('Readjusting valve from ' + str(cv_green) + ' to ' + str(target_angle) + ' degrees')
                    audioControl.play_valve_wrong()
                else:
                    log.write('Rotating valve from ' + str(cv_green) + ' to ' + str(target_angle) + ' degrees')
                audioControl.play_valve_detected(cv_green)
                rotate = rotate_calc(target_angle, cv_green)
                s.c_d = devices.Small(cv_ori)
                s.set_hebiall(s.c_d.hebi0, s.c_d.hebi1 + theta1, s.c_d.hebi2 + theta2)
                if cv_ori == "V":
                    s.set_z(s.c_d.z1 + up)
                    s.set_y(s.c_d.y1)
                    s.set_hebi2(s.hebi2 + rotate*slip_small)
                elif cv_ori == "H":
                    s.set_z(s.c_d.z0)
                    s.set_y(s.c_d.y0 - up)
                    s.set_z(s.c_d.z1)
                    s.set_hebi2(s.hebi2 + rotate)
                    s.set_z(s.c_d.z0)
                if hand_input:
                    break
                s.set_y(rest_y)
                s.set_z(rest_z)
                s.set_hebiall(rest_hebi0, rest_hebi1, rest_hebi2)
                count += 1
                log.write('Computer vision initiated...')
                (dc1, cv_green, dc2) = cvc.processCommand(mission[1])
            audioControl.play_valve_correct()
            music_on = False
            log.write('Valve angle is now within allowable region')
        
        #BIG VALVE
        elif (mission[1] == "V2"): 
            count = 0
            target_angle = int(mission[2])
            audioControl.play_valve_target(target_angle)
            while (((abs(rotate_calc(target_angle, cv_green)) > max_angle_diff) and count <= max_feedback) or (count == 0)):
                if count != 0:
                    log.write('Readjusting valve from ' + str(cv_green) + ' to ' + str(target_angle) + ' degrees')
                    audioControl.play_valve_wrong()
                else:
                    log.write('Rotating valve from ' + str(cv_green) + ' to ' + str(target_angle) + ' degrees')
                audioControl.play_valve_detected(cv_green)
                rotate = target_angle - cv_green
                s.c_d = devices.Big()
                s.set_hebiall(s.c_d.hebi0, s.c_d.hebi1 + theta1, s.c_d.hebi2 + theta2 + cv_green)
                s.set_z(s.c_d.z1 + up)
                s.set_y(s.c_d.y1)
                s.rotate_hebi2(rotate*slip_big)
                if hand_input:
                    break
                s.set_y(rest_y)
                s.set_z(rest_z)
                s.set_hebiall(rest_hebi0, rest_hebi1, rest_hebi2)
                first_rotate = True
                log.write('Computer vision initiated...')
                (dc1, cv_green, dc2) = cvc.processCommand(mission[1])
                count += 1
            audioControl.play_valve_correct()
            music_on = False
            log.write('Valve angle is now within allowable region')
            
        #BREAKERS
        elif (mission[1] == "A" or mission[1] == "B"):
            target = mission[2]
            audioControl.play_breaker(target)
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
                theta2 += 90
            log.write('Flipping switch ' + target)
            y_in = s.c_d.y0
            if abs(cv_off) > 59: #sag compensation
                y_in -= abs(cv_off)/20
            s.set_z(s.c_d.z0+up)
            s.set_hebiall(s.c_d.hebi0, s.c_d.hebi1+theta1, s.c_d.hebi2+theta2)
            s.set_y(y_in)
            s.set_z(s.c_d.z1+up)
            music_on = True
            
        #SHUTTLECOCK
        elif (mission[1] == "V3"):
            target = int(mission[2])
            if (((target == 0) and (cv_green == 0)) or ((target == 1) and (cv_green == 1))):
                audioControl.play_shuttlecock(2)
                log.write('Shuttlecock valve is already in desired position')
                music_on = False
            else:
                audioControl.play_orientation(cv_ori)
                audioControl.play_shuttlecock(target)
                s.c_d = devices.Shuttle(cv_ori)
                if (cv_ori == "V"):
                    s.set_z(s.c_d.z0 + up)
                    if (target == 0):
                        log.write('Opening vertical shuttlecock valve')
                        s.set_hebiall(s.c_d.hebi0c, s.c_d.hebi1c + theta1, s.c_d.hebi2c + theta2)
                        s.set_y(s.c_d.y0)
                        s.rotate_hebi2(-shuttle_rotate)
                    elif (target == 1):
                        log.write('Closing vertical shuttlecock valve')
                        s.set_hebiall(s.c_d.hebi0o, s.c_d.hebi1o + theta1, s.c_d.hebi2o + theta2)
                        s.set_y(s.c_d.y0)
                        s.rotate_hebi2(shuttle_rotate)
                    else:
                        print("Invalid shuttle target")
                elif (cv_ori == "H"):
                    s.set_z(s.c_d.z0)
                    if (target == 0):
                        log.write('Opening horizontal shuttlecock valve')
                        s.set_hebiall(s.c_d.hebi0c, s.c_d.hebi1c + theta1, s.c_d.hebi2c + theta2)
                        s.set_y(s.c_d.y0-up)
                        s.set_z(s.c_d.z1)
                        s.rotate_hebi2(-shuttle_rotate)
                        s.set_z(s.c_d.z0)
                    elif (target == 1):
                        log.write('Closing horizontal shuttlecock valve')
                        s.set_hebiall(s.c_d.hebi0o, s.c_d.hebi1o + theta1, s.c_d.hebi2o + theta2)
                        s.set_y(s.c_d.y0-up)
                        s.set_z(s.c_d.z1)
                        s.rotate_hebi2(shuttle_rotate)
                        s.set_z(s.c_d.z0)
                    else:
                        print("Invalid shuttle target")
                music_on = True
        else:
            print("Invalid device")
        print("Finished Engaging Device: " + s.c_d.name + " at station "
              + s.c_s + " with orientation " + cv_ori)
        if (s.c_d.name == "Small" or s.c_d.name == "Big"):
            print("From angle: " + str(cv_green) + " to " + mission[2] + ". Rotate by: " + str(rotate))
        print("REST POSITION:")
        log.newline()
        s.set_y(rest_y)
        s.set_z(rest_z)
        s.set_hebiall(rest_hebi0, rest_hebi1, rest_hebi2)

log.terminate()
time.sleep(1)
audioControl.play_terminate()
if not debug:
    s.hebi_terminate()
    s.drive_terminate()
    s.stepper_terminate()
time.sleep(2)
