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
from cherrypy.process import plugins

current_dir = os.path.dirname(os.path.abspath(__file__))

serialPort = '/dev/ttyUSB0'

class autonomousController(object):
  
  def __init__(self):
    self.exitFlag = False
    
    self.piCam = camera.Camera()

    self.piCam.start()

    self.sonar1 = sonar.Sonar(trig=23, echo=24)
    self.sonar1.start()

    self.iRobot = create.Create(serialPort)

    self.sensorArray = False

    self.robotController = control.Control(self.iRobot,self.piCam,self.sonar1,self.sensorArray)

    self.robotController.start()

  def validRequest(self):
    if self.exitFlag == False:
      return True
    else:
      return False
      
  
  def stop(self):
    self.exitFlag = True
    
    self.robotController.stop()
    self.piCam.stop()
    self.sonar1.stop()
    cherrypy.engine.stop()
    cherrypy.engine.exit()
    
    

  @cherrypy.expose
  def getImage(self, random):
      if self.validRequest() == False: 
        print("ended")
        return
      # print(piCam.image)
      cherrypy.response.headers['Content-Type'] = 'image/jpeg'
      return cv2.imencode('.jpg', self.piCam.image)[1].tostring()

  @cherrypy.expose
  def getSensor(self, sensor):
    if self.validRequest() == False: 
      return
    if sensor == "sonar":
      return str(self.sonar1.currentDistance)


  @cherrypy.expose
  def move(self, num):
    if self.validRequest() == False: 
      return
    #print("test " + str(num))
    self.robotController.changeVel(int(num))

  @cherrypy.expose
  def turn(self, num):
    if self.validRequest() == False: 
      return
    #print("test " + str(num))
    self.robotController.changeTurn(int(num))
    
  @cherrypy.expose
  def auto(self, val):
    if self.validRequest() == False: 
      return
    #print("test " + str(num))
    if val == "true":
      self.robotController.enableAuto()
    else:
      self.robotController.disableAuto()



  @cherrypy.expose
  def cleanslateprotocol(self):
    if self.validRequest() == False: return
    
    self.stop()
    
   

  @cherrypy.expose
  def index(self):
    if self.validRequest() == False:
      return
	  
    return serve_file(os.path.join(current_dir, 'webfiles/html', 'index.html'),content_type='text/html')




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

# my_feature = autonomousController(cherrypy.engine)
# my_feature.subscribe()
# cherrypy.tree.mount(my_feature)
cherrypy.quickstart(autonomousController(), config=conf)

