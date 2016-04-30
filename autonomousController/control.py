import sys
sys.path.append('/home/pi')
sys.path.append('../pycreate')
# import the necessary packages
import time
import math
import threading
from autonomousController import utilities
import create
 
class Control(threading.Thread):

	def __init__(self, iRobot, camera, sonar, sensorArray):
		self.iRobot = iRobot
		self.camera = camera
		self.sonar = sonar
		self.sensorArray = sensorArray
		self.directionalVel = 0
		self.rotationalVel = 0


		#Set up threading
		self.exitFlag = False
		threading.Thread.__init__(self)
		self.threadID = 600
		self.name = "iRobot Control"

	
	def changeVel(self,num):
		self.directionalVel = num	

	def changeTurn(self, num):
		self.rotationalVel = num
	 
	def run(self):
		# capture frames from the camera
		while self.exitFlag == False:
			angle = self.camera.angle
			if abs(angle) > 2:			
				self.rotationalVel = math.copysign(1.0, angle) * -10
			else:
				self.rotationalVel = 0

			print("angle " + str(angle) + " rotate " + str(self.rotationalVel))
			print("speed" + str(self.directionalVel))




			self.iRobot.go(self.directionalVel,self.rotationalVel)
			
			#print(self.directionalVel)
			time.sleep(.01)




	def stop(self):
		self.exitFlag = True





