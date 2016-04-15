import RPi.GPIO as GPIO
import time

import threading
from autonomousController import utilities

'''
Sonoar class manages reading distance information from a sonar sensor connected to TRIG and ECHO gpio
pins on a Raspberry Pi.  Tested on Raspberry Pi Model B
@input trig [number GPIO pin using GPIO.BCM mode] [represents pin connected to sonar trigger]
@input echo [number GPIO pin using GPIO.BCM mode] [represents pin connected to sonar echo]
'''
class Sonar(threading.Thread):

	def __init__(self, trig, echo, senseDelay=0.001):
		self.TRIG = trig
		self.ECHO = echo
		self.senseDelay = senseDelay

		#Set GPIO and pins for trigger and echo
		GPIO.setmode(GPIO.BCM)
		self.TRIG = trig
		self.ECHO = echo
		GPIO.setup(self.TRIG,GPIO.OUT)
		GPIO.setup(self.ECHO,GPIO.IN)
		GPIO.output(self.TRIG, False)
		time.sleep(2) #delay to ensure sensor is ready

		#currentDistance will hold the last measured distance when continuously measuring distance
		#continuous distance measurement is initialized by sonar.start()  See python threading documentation.
		self.currentDistance = -1 #distance is in cm

		#Set up thread
		threading.Thread.__init__(self)
		self.threadID = self.ECHO
		self.name = "echo" + str(self.ECHO) + "trig" + str(self.TRIG)
		#Thread exits when sent to True
		self.exitFlag = False
		
		utilities.log("Sonar Initialized")

	def __exit__(self):
		GPIO.cleanup()


	def getMeasurement(self):
			GPIO.output(self.TRIG, True)
			time.sleep(0.00001)
			GPIO.output(self.TRIG, False)
			pulse_start=1
			pulse_end=0

			while GPIO.input(self.ECHO)==0:
			  pulse_start = time.time()

			while GPIO.input(self.ECHO)==1:
			  pulse_end = time.time()

			distance = round((pulse_end - pulse_start) * 17150, 2)

			# log("Distance:"+str(distance) + "cm",10)

			return distance

	def run(self):
		while self.exitFlag == False:
			self.currentDistance = self.getMeasurement()
			utilities.log("sonar distance " + str(self.currentDistance))
			time.sleep(self.senseDelay)

		GPIO.cleanup()

	def stop(self):
		self.exitFlag = True



if __name__ == '__main__':
	sonar1 = Sonar(trig=23, echo=24)
	sonar1.start()
	lim=0
	while lim<100:
		print(sonar1.currentDistance)
		time.sleep(.1)
		lim+=1

	sonar1.stop()













