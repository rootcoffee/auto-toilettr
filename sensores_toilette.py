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
rele1 = 18	# azul / bano mujeres
rele2 = 17 	# verde / Luz emergencia / always on
rele3 = 24      # amarillo / ozonizador
rele4 = 23      # naranja / bano hombres
pir1 = MotionSensor(4)
pir2 = MotionSensor(27)

#setup the pins
GPIO.setup(rele1, GPIO.OUT)
GPIO.setup(rele2, GPIO.OUT)
GPIO.setup(rele3, GPIO.OUT)
GPIO.setup(rele4, GPIO.OUT)

ON = GPIO.LOW
OFF = GPIO.HIGH

GPIO.output(rele1,  OFF)
GPIO.output(rele2,  OFF)
GPIO.output(rele3,  OFF)
GPIO.output(rele4,  OFF)

# Flash all reles for a couple of secs to test
GPIO.output(rele1,  ON)
time.sleep(1)
GPIO.output(rele1,  OFF)
GPIO.output(rele2,  ON)
time.sleep(1)
GPIO.output(rele2,  OFF)
GPIO.output(rele3,  ON)
time.sleep(1)
GPIO.output(rele3,  OFF)
GPIO.output(rele4,  ON)
time.sleep(1)
GPIO.output(rele4,  OFF)


# Luz de emergencia siempre encendida
GPIO.output(rele2,  ON)


# Define global vars
tmoutvalue = 300
sleeptime = 1
tmoutpir1 = tmoutvalue
tmoutpir2 = tmoutvalue
pir1flag = 0
pir2flag = 0
rele3flag = 0


# This script will monitor for movement in two bathrooms,
# and will activate lights, fan and an ozonifier by means of electrical reles.
# The ozonifier will be connected by a common rele, and will be activated by
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
					GPIO.output(rele1,  ON)
					#print("Rele 1 enabled")
					pir1flag = 1
					tmoutpir1 = tmoutvalue

					GPIO.output(rele3, ON)
					rele3flag = 1


			if pir2.motion_detected:
					#print("move detected in sensor 2")
					GPIO.output(rele4,  ON)
					#print("Rele 4 enabled")
					pir2flag = 1
					tmoutpir2 = tmoutvalue

					GPIO.output(rele3, ON)
					rele3flag = 1


			if pir1flag == 0 and pir2flag == 0:
					if rele3flag == 1:
							GPIO.output(rele3, OFF)
							rele3flag = 0
							#print("Rele 3 disabled")

			if tmoutpir1==0:
					GPIO.output(rele1, OFF)
					pir1flag = 0
					tmoutpir1 = tmoutvalue
					#print("Rele 1 disabled")

			if tmoutpir2==0:
					GPIO.output(rele4, OFF)
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
