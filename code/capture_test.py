# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 19:31:20 2017

@author: Michu
"""

import picamera
import capture

camera = picamera.PiCamera()

device = "V2"

(cv_off, cv_green, cv_ori) = capture.cv_info(camera, device)

print cv_off
print cv_green
print cv_ori