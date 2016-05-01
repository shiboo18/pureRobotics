'''
Created by Nathan Morin @nathanamorin nathanmorin.com
as part of Purdue University CIT 581 Robotics
'''
# import RPi.GPIO as GPIO
import time
import sys
sys.path.append('../pycreate')
import numbers
import create
import sense
import threading

'''
Manages access to virtualSensors for an iRobot Create
virtualSensors are single or sets of cooperative virtualSensors with a single max/min value and triggered funciton
triggered funciton must have parameter which is the virtual sensor which triggered the funciton
Sample use case:
    virtualSensors = robotvirtualSensorArray()
    virtualSensors.attachvirtualSensor([["CURRENT",True (true shows the state to check against)]], 6,24,lambda: runWhenBadBattery)
    ##Information about lambda : http://stackoverflow.com/questions/803616/passing-functions-with-arguments-to-another-function-in-python
    virtualSensors.start()

    ... other functions & etc.

    virtualSensors.stop()
'''
class VirtualSensorArray(threading.Thread):

    port = '/dev/ttyUSB0'

    class virtualSensor():
        def __init__(self, names, trigFunc, minVal=False, maxVal=False, validateFunc=False, senseDelay=0.001):
            self.names = names
            self.minVal = minVal
            self.maxVal = maxVal
            self.trigFunc = trigFunc
            self.validateFunc = validateFunc
            self.senseDelay = senseDelay
            self.currentVal = {}
        
        def updateVirtualSensor(self, senseVals):
            self.currentVal = senseVals
            numTriggered = 0
            for name in self.names:
                currentValTemp = self.currentVal[name[0]]
                if self.validateFunc != False:
                    if self.validateFunc(currentValTemp) == name[1]:
                        numTriggered+=1
                                
                elif isinstance(currentValTemp, numbers.Number):
                    raise
                    #Trigger function when value is out of range
                    if (currentValTemp < minVal or currentValTemp > maxVal) == name[0]:
                        numTriggered += 1
            
            if numTriggered != 0 and numTriggered == len(self.names):
                self.trigFunc()
                        
                        
        # def getVirtualSensor(self,retrievalMethod):
            
        #     for name in self.names:
        #          self.currentVal[name] = retrievalMethod(name)
            
        #     self.updatevirtualSensor()
                 

    def __init__(self, iRobot=False, id=1, name="sensorArray"):
        if iRobot == False:
            iRobot = create.Create(port)
        self.iRobot = iRobot
        self.virtualSensorList = []
        threading.Thread.__init__(self)
        threading.threadID = id
        threading.name = name
        self.exitFlag = False
        
    
    def attachVirtualSensor(self, names, trigFunc, minVal=False, maxVal=False,validateFunc=False, senseDelay=0.001):
        tempvirtualSensor = self.virtualSensor(names,trigFunc, minVal,maxVal,validateFunc,senseDelay)
        self.virtualSensorList.append(tempvirtualSensor)
        
        
    def __exit__(self):
        pass
        
    def run(self):
        while self.exitFlag == False:
            #Retrive sensor data from iRobot
            self.currentVals = sense.sensor_dict_list(self.iRobot, 'BUMPS_AND_WHEEL_DROPS', \
                                        sense.BUMP_AND_WHEEL_DROP_KEYS)
            #Update virtual sensors 
            for vs in self.virtualSensorList:
                vs.updateVirtualSensor(self.currentVals)
                
                
    def stop(self):
        self.exitFlag = True

















