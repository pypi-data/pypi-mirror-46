#!/usr/bin/python

from time import sleep, strftime
from picamera import PiCamera

#define camera parameters
camera = PiCamera()
camera.resolution = (3280, 2464)
camera.iso = 100
# Wait for the automatic gain control to settle
sleep(2)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g



camera.start_preview()
# Camera warm-up time
sleep(2)
curr_time = strftime("%Y%m%d-%H%M%S")
camera.capture('/home/pi/Pictures/image_%s.jpg' % curr_time)
camera.stop_preview()
