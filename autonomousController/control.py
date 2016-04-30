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
		self.auto = False
		self.iRobot = iRobot
		self.camera = camera
		self.sonar = sonar
		self.sensorArray = sensorArray
		self.directionalVel = 0
		self.rotationalVel = 0
		self.distHistory = [0]
		self.freq = 0.01


		#Set up threading
		self.exitFlag = False
		threading.Thread.__init__(self)
		self.threadID = 600
		self.name = "iRobot Control"

	
	def changeVel(self,num):
		self.directionalVel = num	
		
	def enableAuto(self):
		self.auto = True
	
	def disableAuto(self):
		self.auto = False

	def changeTurn(self, num):
		self.rotationalVel = num
	 
	def run(self):
		
		measuredFreq = time.time()
		
		while self.exitFlag == False:
			measuredFreq = time.time() - measuredFreq
			if self.auto == True:
				angle = self.camera.angle
				if abs(angle) > 2:			
					self.rotationalVel = math.copysign(1.0, angle) * -10
				else:
					self.rotationalVel = 0
				
				dist = self.sonar.currentDistance
				
				
				distDela = dist - 10.0#sum(self.distHistory) / float(len(self.distHistory))
				
				#self.directionalVel = distDela * 100.0 / 10.0#max(measuredFreq, self.freq)
				if distDela > 10:
					self.directionalVel = 10
				else:
					self.directionalVel = 0
				
				# self.distHistory.append(dist)
				
				# if len(self.distHistory) > 1000:
				# 	self.distHistory.pop(0)

				#print("angle " + str(angle) + " rotate " + str(self.rotationalVel))
				print("speed" + str(self.directionalVel))




			self.iRobot.go(self.directionalVel,self.rotationalVel)
			
			#print(self.directionalVel)
			time.sleep(self.freq)




	def stop(self):
		print("stoping robot controller")
		self.exitFlag = True





