#!/usr/bin/python

from time import sleep, strftime
from picamera import PiCamera
from gpiozero import Button
import pigpio
camera = PiCamera()
pi = pigpio.pi()


#define parameters
intensity = 10
led_pwm_pin = 12
button = Button(16)
camera.resolution = (3280, 2464)
# camera.iso = 100
#
# # Wait for the automatic gain control to settle
# sleep(2)
# # Now fix the values
# camera.shutter_speed = camera.exposure_speed
# camera.exposure_mode = 'off'
# g = camera.awb_gains
# camera.awb_mode = 'off'
# camera.awb_gains = g


while True:
    camera.start_preview()
    pi.hardware_PWM(led_pwm_pin,50000,intensity*10000)
    try:
        button.wait_for_press()
        curr_time = strftime("%Y%m%d-%H%M%S")
        camera.capture('/home/pi/Pictures/image_%s.jpg' % curr_time)
    except KeyboardInterrupt:
        camera.stop_preview()
        pi.hardware_PWM(led_pwm_pin,50000,0000)
        break
