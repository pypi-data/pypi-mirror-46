#!/usr/bin/python

from time import sleep, strftime
from picamera import PiCamera
from gpiozero import Button
import pigpio
camera = PiCamera()
pi = pigpio.pi()


#define parameters
intensity = 1
led_pwm_pin = 12
button = Button(16)
button1 = Button(20)
camera.resolution = (3280, 2464)
#camera.iso = 100
camera.hflip = True
camera.vflip = True
# Wait for the automatic gain control to settle
#sleep(2)
# Now fix the values
# camera.shutter_speed = camera.exposure_speed
# camera.exposure_mode = 'off'
# g = camera.awb_gains
# camera.awb_mode = 'off'
# camera.awb_gains = g


while True:
    #screen resolution = 800x480 pixels
    #window=(x,y,w,h)

    pi.hardware_PWM(led_pwm_pin,50000,intensity*10000)
    try:
	#2.2 inch
        camera.start_preview(fullscreen=False,window=(200,100,352,211))
	sleep(0.2)
        button.wait_for_press()
        camera.start_preview(fullscreen=False,window=(165,75,448,269))
	sleep(0.2)
        button.wait_for_press()
        camera.start_preview(fullscreen=False,window=(100,40,560,336))
	sleep(0.2)
        button.wait_for_press()
        camera.start_preview(fullscreen=False,window=(0,0,800,480))
	sleep(0.2)
        button.wait_for_press()
	#button1.wait_for_press()
        #curr_time = strftime("%Y%m%d-%H%M%S")
        #camera.capture('/home/pi/Pictures/image_%s.jpg' % curr_time)
    except KeyboardInterrupt:
        camera.stop_preview()
        pi.hardware_PWM(led_pwm_pin,50000,0000)
        break
