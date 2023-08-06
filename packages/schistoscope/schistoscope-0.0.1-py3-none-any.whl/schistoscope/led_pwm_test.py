import pigpio
import time

pi = pigpio.pi()

while True:
		duty = input("Input brightness (0-100): ")
		pi.hardware_PWM(12,50000,duty*10000)
		time.sleep(0.5)
	
 
