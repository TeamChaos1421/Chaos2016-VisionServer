#!/usr/bin/python

import socket
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(1)

# Engage Motors
ser.write('G91\n')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 5800))

while 1:
	s.send('GET\n')
	data = s.recv(1024)
	
	values = map(int, data.split(" "))
	print values
	
	ser.flushInput()
	if(abs(values[0]) > 5):
		ser.write('G1 X'+str(values[0]*0.005)+'\n')
	if(abs(values[1]) > 5):
		ser.write('G1 Y'+str(values[1]*0.005)+'\n')
	
	time.sleep(0.05)
