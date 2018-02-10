# Imports
import os
import time
import RPi.GPIO as GPIO
from gpiozero import MotionSensor

# setting a current mode
GPIO.setmode(GPIO.BCM)
#removing the warings
#GPIO.setwarnings(False)

#define the pins
rele1 = 18
rele2 = 17
rele3 = 15
rele4 = 14
pir1 = MotionSensor(4)
pir2 = MotionSensor(27)

#setup the pins
GPIO.setup(rele1, GPIO.OUT)
GPIO.setup(rele2, GPIO.OUT)
GPIO.setup(rele3, GPIO.OUT)
GPIO.setup(rele4, GPIO.OUT)

GPIO.output(rele1,  GPIO.HIGH)
GPIO.output(rele2,  GPIO.HIGH)
GPIO.output(rele3,  GPIO.HIGH)
GPIO.output(rele4,  GPIO.LOW)

# Define global vars
tmoutvalue = 60
sleeptime = 1
tmoutpir1 = tmoutvalue
tmoutpir2 = tmoutvalue
pir1flag = 0
pir2flag = 0
rele3flag = 0


# This script will monitor for movement in two bathrooms,
# and will activate lights, fan and an ozonifier by means of electrical reles.
# The last one will be connected by a common rele, and will be activated by
# move on any bathroom.
# The seconds for auto off is setup as tmoutvalue global var.

try:
	while True:
			time.sleep(sleeptime)

			if pir1flag==1:
					tmoutpir1 -= 1
			if pir2flag==1:
					tmoutpir2 -= 1

			if pir1.motion_detected:
					#print("move detected in sensor 1")
					GPIO.output(rele1,  GPIO.LOW)
					#print("Rele 1 enabled")
					pir1flag = 1
					tmoutpir1 = tmoutvalue

					GPIO.output(rele3,  GPIO.LOW)
					rele3flag = 1


			if pir2.motion_detected:
					#print("move detected in sensor 2")
					GPIO.output(rele2,  GPIO.LOW)
					#print("Rele 2 enabled")
					pir2flag = 1
					tmoutpir2 = tmoutvalue

					GPIO.output(rele3,  GPIO.LOW)
					rele3flag = 1


			if pir1flag == 0 and pir2flag == 0:
					if rele3flag == 1:
							GPIO.output(rele3,  GPIO.HIGH)
							rele3flag = 0
							#print("Rele 3 disabled")

			if tmoutpir1==0:
					GPIO.output(rele1,  GPIO.HIGH)
					pir1flag = 0
					tmoutpir1 = tmoutvalue
					#print("Rele 1 disabled")

			if tmoutpir2==0:
					GPIO.output(rele2,  GPIO.HIGH)
					pir2flag = 0
					tmoutpir2 = tmoutvalue
					#print("Rele 2 disabled")

			# Print status
			os.system('clear')
			print('Status:')
			print('PIR sensor 1: ', pir1flag)
			print('    TMOUT 1: ', tmoutpir1, '\n')
			print('PIR sensor 2: ', pir2flag)
			print('    TMOUT 2: ', tmoutpir2, '\n')
			print('Rele 3: ', rele3flag, '\n')
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
