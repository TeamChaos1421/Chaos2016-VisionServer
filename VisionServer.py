#!/usr/bin/python

# For the CV Part
import numpy as np
import cv2

# For the Server Part
import threading
import socket
import time

# Globals for Temporary Data Storage
data_flag = False
data = "0 0"

# OpenCV Thread Class Definition
class CVThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	# For Reasons
	def nothing(self, x):
		pass

	def run(self):
		
		# Globals
		global data_flag
		global data
		
		# Open the Camera Stream
		cam = cv2.VideoCapture(1)

		# Create Windows
		cv2.namedWindow('Threshed Image')
		cv2.namedWindow('Rendered Image')

		# Create Trackbars for Thresholding
		cv2.createTrackbar('H-','Threshed Image',0,255,self.nothing)
		cv2.createTrackbar('H+','Threshed Image',0,255,self.nothing)
		cv2.createTrackbar('S-','Threshed Image',0,255,self.nothing)
		cv2.createTrackbar('S+','Threshed Image',0,255,self.nothing)
		cv2.createTrackbar('V-','Threshed Image',0,255,self.nothing)
		cv2.createTrackbar('V+','Threshed Image',0,255,self.nothing)
		
		while 1:
			# Get Image from Camera
			ret, image = cam.read()
			
			# There is an Escape
			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				break

			# Get Trackbar Positions
			rn = cv2.getTrackbarPos('H-','Threshed Image')
			rp = cv2.getTrackbarPos('H+','Threshed Image')
			gn = cv2.getTrackbarPos('S-','Threshed Image')
			gp = cv2.getTrackbarPos('S+','Threshed Image')
			bn = cv2.getTrackbarPos('V-','Threshed Image')
			bp = cv2.getTrackbarPos('V+','Threshed Image')

			# Blur the Image (for science)
			hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
			blur = cv2.GaussianBlur(hsv,(5,5),0)
			
			# Generate mask of pixels whose color falls into our desired ranges.
			mask = cv2.inRange(blur,np.array([bn,gn,rn]),np.array([bp,gp,rp]))

			# Generate Contours from Mask
			ignore, contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

			# Assume nothing is there
			something = False
			
			# Iterate Over Every Contour
			for contour in contours:

				# Only Deal With Large Contours
				if(cv2.contourArea(contour) > 5000):
					
					# Assumption Wrong
					something = True
					
					# Find Centroid Position With Respect to the Image Center
					M = cv2.moments(contour)    
					cx = int(M['m10']/(M['m00']+0.1))-320
					cy = 240-int(M['m01']/(M['m00']+0.1))

					# Render Contour
					cv2.drawContours(image,[contour],-1,(0,255,0),3)
					
					# Store Position for Other Threads
					data_flag = True
					data = str(cx) + " " + str(cy)
					data_flag = False
				
			if not something:
				# Store (Fake) Position for Other Threads is nothing there
				data_flag = True
				data = "0 0"
				data_flag = False
					
			
			# Display Image with Overlay
			cv2.imshow('Rendered Image',image)

			# Render and Display Thresholded Image
			threshed = cv2.bitwise_and(image,image,mask=mask)
			cv2.imshow('Threshed Image', threshed)


# Naive Server Thread Class Definition
class ServerThread_Single (threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
	
	def run(self):
		# Start Listening On Port 5800
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('0.0.0.0', 5801))
		s.listen(1)
		
		# Accept Connections
		while 1:
			conn, addr = s.accept()
			
			# Avoid Race Condition	
			while data_flag:
				pass
			
			# Send Data and Close Connection
			conn.send(data)
			conn.close()
			
# Better Server Thread Class Definition
class ServerThread_Continuous (threading.Thread):

	def __init__(self, connection, address):
		threading.Thread.__init__(self)
		self.connection = connection
		self.address = address
	
	def run(self):
		
		while 1:
			# Get Token Amount Of Data
			ignore = self.connection.recv(20)
			if not ignore: break
			
			# Avoid Race Condition	
			while data_flag:
				pass
			
			# Send Data
			self.connection.send(data+"\n")
			
			# Wait
			time.sleep(0.01)
		
		# Close Connection When Done
		self.connection.close()



# Create Threads
cvThread = CVThread()
serverThread_Single = ServerThread_Single()

# Start Threads
cvThread.start()
serverThread_Single.start()



# Start Listening On Port 5800
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 5800))
s.listen(1)

while 1:
	# Accept Connections
	conn, addr = s.accept()
	
	serverThread_Continuous = ServerThread_Continuous(conn, addr)
	serverThread_Continuous.start()
