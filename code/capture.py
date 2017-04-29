# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 20:04:18 2017

@author: Michu
"""

from DeviceRecognition import *
import picamera

# static flag to enable picamera code
USE_CAMERA = True
MOCK_IMG_PATH = "cvimages/image26.jpg"
#MOCK_IMG_PATH = "imgs/shuttlecock_lowres.jpg"
capture_path = "imgs/capture.jpg"

def cv_info(camera, device_code = "none"):
	if device_code == "none":
		device_code = raw_input("Device Type: ")
		# Case on extracted device code!
  
	if (device_code == "V1"):
		device = ValveSmall()
	elif (device_code == "V2"):
		# device is large valve
		device = ValveLarge()
	elif (device_code == "V4"):
		# device is shuttlecock
		device = Shuttlecock()
	elif (device_code == "B"):
		# device is breaker box
		device = BreakerBox()
	else:
		return (0, 0, "V")
  
	if USE_CAMERA:
		camera.capture(capture_path,format = 'jpeg')
		path = capture_path
	else:
		path = MOCK_IMG_PATH

	retval = device.processImage(path)

	if not retval:
		print ("Detect FAILED!")
		#self.writeData(0,0,0)
		return
	else:
		print ("Successful detection!")
		(offset,orient,angle) = retval
		print(offset)
  		print(angle)
		#self.writeData(offset,orient,angle)
		return (offset, angle, orient)