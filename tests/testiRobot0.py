import serial
import time

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

ser.write('\x80')

time.sleep(.1)

ser.write('\x83')

time.sleep(.1)

ser.write('\x91\xFF\x36\xFF\x36')

ser.close()