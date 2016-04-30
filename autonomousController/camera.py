import sys
sys.path.append('/home/pi')
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import threading
from autonomousController.detect_lane_houghlinesP import *
from autonomousController.config_lane import *
from autonomousController import utilities
 
class Camera(threading.Thread):

	def __init__(self):
		
		
		self.image = []
		self.angle = 0
		
		# initialize the camera and grab a reference to the raw camera capture
		self.camera = PiCamera()
		self.camera.resolution = (640, 480)
		self.camera.framerate = 32
		self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
		time.sleep(0.1)

		#Set up thread
		threading.Thread.__init__(self)
		self.threadID = 100
		self.name = "camera"
		#Thread exits when sent to True
		self.exitFlag = False
	 
	def run(self):
		# capture frames from the camera
		for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
			# grab the raw NumPy array representing the image, then initialize the timestamp
			# and occupied/unoccupied text
			self.image = frame.array
		 
			# show the frame
			# cv2.imshow("Frame", image)
			gb_lane_cfg = LaneCfg
			proc = {'houghlinesP':detect_lane_over_houghlinesP}
			self.angle = proc[gb_lane_cfg['set']['proc']](gb_lane_cfg['set']['proc'], self.image, gb_lane_cfg)


			#utilities.log("angle " + str(self.angle))
		 
			# clear the stream in preparation for the next frame
			self.rawCapture.truncate(0)
		 
			# if the `q` key was pressed, break from the loop
			if self.exitFlag == True:
				break

	def stop(self):
		self.exitFlag = True


if __name__ == '__main__':
	piCam = Camera()
	piCam.start()


