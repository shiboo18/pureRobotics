import sys
sys.path.append('/home/pi')

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))


import random
import string
import cv2
from camera import Camera

import cherrypy

class autonomousController(object):

  @cherrypy.expose
  def getImage(self, random):
      print(piCam.image)
      cherrypy.response.headers['Content-Type'] = 'image/jpeg'
      return cv2.imencode('.jpg', piCam.image)[1].tostring()

  @cherrypy.expose
  def cleanslateprotocol(self):
    cherrypy.engine.exit()
    piCam.stop()



piCam = Camera()

piCam.start()

cherrypy.server.socket_host = '0.0.0.0'
cherrypy._cpconfig.Config(file="cherrypyConfig.conf")
cherrypy.quickstart(autonomousController())

