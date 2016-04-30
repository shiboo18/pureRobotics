import sys
sys.path.append('../pycreate')

import create
import move

iRobot = create.Create('/dev/ttyUSB0')


SENSOR_KEYS = [     # sensor keys with single return value
   # 'CLIFF_LEFT_SIGNAL',
   # 'CLIFF_FRONT_LEFT_SIGNAL',
   # 'CLIFF_FRONT_RIGHT_SIGNAL',
   # 'CLIFF_RIGHT_SIGNAL',
   # 'WALL_SIGNAL',
   # 'DISTANCE',
   # 'ANGLE',
   # 'IR_BYTE',
   # 'VOLTAGE',
   # 'OI_MODE',
   # 'SONG_PLAYING',
   # 'SONG_NUMBER',
   # 'VIRTUAL_WALL',
   # 'CHARGING_STATE',
   # 'CURRENT',
   # 'BATTERY_TEMPERATURE',
   # 'BATTERY_CHARGE',
   # 'BATTERY_CAPACITY',
   # 'NUMBER_OF_STREAM_PACKETS',
   # 'CHARGING_SOURCES_AVAILABLE',
   # 'WALL',
   # 'CLIFF_LEFT',
   # 'CLIFF_FRONT_LEFT',
   # 'CLIFF_FRONT_RIGHT',
   # 'CLIFF_RIGHT',
   'BUMP_RIGHT',
   'BUMP_LEFT'
   # 'VELOCITY',
   # 'RADIUS',
   # 'RIGHT_VELOCITY',
   # 'LEFT_VELOCITY'
    ]

while True:
	#for key in SENSOR_KEYS:
	#	print (key + "\t\t" +  str(iRobot.getSensor(key)) + '\r')
	iRobot.sense()
	print(iRobot.bump_left)
