# Imports
import threading
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

GPIO.output(rele1,  GPIO.LOW)
GPIO.output(rele2,  GPIO.LOW)
GPIO.output(rele3,  GPIO.LOW)
GPIO.output(rele4,  GPIO.LOW)

# Define global vars
tmoutvalue = 3
sleeptime = 5
tmoutpir1 = tmoutvalue
tmoutpir2 = tmoutvalue
pir1flag = 0
pir2flag = 0


class releLuz(object):
	def __init__(self, interval=10):
			""" Constructor
			:type interval: int
			:param interval: Check interval, in seconds
			"""
			self.interval = interval

			thread = threading.Thread(target=self.run, args=())
			thread.daemon = True                            # Daemonize thread
			thread.start()                                  # Start the execution
			
	def run(self):
		""" Method that runs forever """
			
		print('Esperando para apagar el rele: ' + object)

		time.sleep(self.interval)
		GPIO.output(object,  GPIO.LOW)

		print('Rele: ' + object + ' apagado')




# main

releBanoMujeres = releLuz(rele1)
releBanoHombres = releLuz(rele2)


while True:

	if pir1.motion_detected:
		GPIO.output(rele1,  GPIO.HIGH)
		print('Movimiento en pir1. Encendiendo rele1')
		releBanoMujeres.run()

	if pir2.motion_detected:
		GPIO.output(rele2,  GPIO.HIGH)
		print('Movimiento en pir2. Encendiendo rele2')
		releBanoHombres.run()

	



