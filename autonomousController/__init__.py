__all__ = ['camera', 'sonar', 'control']

import sys
sys.path.append('/home/pi')
sys.path.append('./pycreate')
import create
import os.path
import random
import string
import cv2
from autonomousController import *
import cherrypy
from cherrypy.lib.static import serve_file

current_dir = os.path.dirname(os.path.abspath(__file__))

serialPort = '/dev/ttyUSB0'

class autonomousController(object):

  @cherrypy.expose
  def getImage(self, random):
      # print(piCam.image)
      cherrypy.response.headers['Content-Type'] = 'image/jpeg'
      return cv2.imencode('.jpg', piCam.image)[1].tostring()

  @cherrypy.expose
  def getSensor(self, sensor):
    if sensor == "sonar":
      return str(sonar1.currentDistance)


  @cherrypy.expose
  def move(self, num):
    #print("test " + str(num))
    robotController.changeVel(int(num))

  @cherrypy.expose
  def turn(self, num):
    #print("test " + str(num))
    robotController.changeTurn(int(num))



  @cherrypy.expose
  def cleanslateprotocol(self):
    cherrypy.engine.exit()
    piCam.stop()

  @cherrypy.expose
  def index(self):
	  return serve_file(os.path.join(current_dir, 'webfiles/html', 'index.html'),
	  	content_type='text/html')



piCam = camera.Camera()

piCam.start()

sonar1 = sonar.Sonar(trig=23, echo=24)
sonar1.start()

iRobot = create.Create(serialPort)

sensorArray = False

robotController = control.Control(iRobot,piCam,sonar1,sensorArray)

robotController.start()


cherrypy.server.socket_host = '0.0.0.0'
# cherrypy._cpconfig.Config(file= current_dir + "/cherrypyConfig.conf")
cherrypy.log.screen = None
conf = {
        '/':
        {'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))},
          '/js': {
          	'tools.staticdir.on': True,
          	'tools.staticdir.dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webfiles/js/')
          	},
          '/css': {
          	'tools.staticdir.on': True,
          	'tools.staticdir.dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webfiles/css/')
          	},
          '/html': {
          	'tools.staticdir.on': True,
          	'tools.staticdir.dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webfiles/html/')
          	}
        
      }

cherrypy.quickstart(autonomousController(), config=conf)

