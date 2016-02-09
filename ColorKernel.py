import re
from urllib import urlopen
import numpy as np
import cv2

class ColorKernelInteractive:
	# For Reasons
	def nothing(self, x):
		pass
		
	def __init__(self, prefix, dataSemaphore):
		self.prefix = prefix
		self.dataSemaphore = dataSemaphore
		self.dataSemaphore.data = {"cx": 0, "cy": 0}
	
	def init(self):
		
		# Create Windows
		cv2.namedWindow(self.prefix + 'Threshed Image')
		cv2.namedWindow(self.prefix + 'Rendered Image')

		# Create Trackbars for Thresholding
		cv2.createTrackbar('H-',self.prefix + 'Threshed Image',0,255,self.nothing)
		cv2.createTrackbar('H+',self.prefix + 'Threshed Image',0,255,self.nothing)
		cv2.createTrackbar('S-',self.prefix + 'Threshed Image',0,255,self.nothing)
		cv2.createTrackbar('S+',self.prefix + 'Threshed Image',0,255,self.nothing)
		cv2.createTrackbar('V-',self.prefix + 'Threshed Image',0,255,self.nothing)
		cv2.createTrackbar('V+',self.prefix + 'Threshed Image',0,255,self.nothing)
	
	def run(self, image):

		# Get Trackbar Positions
		rn = cv2.getTrackbarPos('H-',self.prefix + 'Threshed Image')
		rp = cv2.getTrackbarPos('H+',self.prefix + 'Threshed Image')
		gn = cv2.getTrackbarPos('S-',self.prefix + 'Threshed Image')
		gp = cv2.getTrackbarPos('S+',self.prefix + 'Threshed Image')
		bn = cv2.getTrackbarPos('V-',self.prefix + 'Threshed Image')
		bp = cv2.getTrackbarPos('V+',self.prefix + 'Threshed Image')

		# Blur the Image (for science)
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		blur = cv2.GaussianBlur(hsv,(5,5),0)
		
		# Generate mask of pixels whose color falls into our desired ranges.
		mask = cv2.inRange(blur,np.array([bn,gn,rn]),np.array([bp,gp,rp]))

		# Generate Contours from Mask
		ignore, contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

		# Assume nothing is there
		self.dataSemaphore.data["useful"] = False
		
		# Iterate Over Every Contour
		for contour in contours:

			# Only Deal With Large Contours
			if(cv2.contourArea(contour) > 5000):
				
				# Assumption Wrong
				self.dataSemaphore.data["useful"] = True
				
				# Find Centroid Position With Respect to the Image Center
				M = cv2.moments(contour)
				self.dataSemaphore.data["cx"] = int(M['m10']/(M['m00']+0.1))-320
				self.dataSemaphore.data["cy"] = 240-int(M['m01']/(M['m00']+0.1))

				# Render Contour
				cv2.drawContours(image,[contour],-1,(0,255,0),3)
				
				# Render Center of Mass
				cv2.circle(image, (int(M['m10']/(M['m00']+0.1)), int(M['m01']/(M['m00']+0.1))), 3, (0,255,0), 2)
				cv2.circle(image, (int(M['m10']/(M['m00']+0.1)), int(M['m01']/(M['m00']+0.1))), 5, (0,0,255), 2)
				cv2.circle(image, (int(M['m10']/(M['m00']+0.1)), int(M['m01']/(M['m00']+0.1))), 7, (0,255,0), 2)
		
		# Display Image with Overlay
		cv2.imshow(self.prefix + 'Rendered Image',image)

		# Render and Display Thresholded Image
		threshed = cv2.bitwise_and(image,image,mask=mask)
		cv2.imshow(self.prefix + 'Threshed Image', threshed)
		
		# Send to Server, regardless of whether it was asked for
		self.dataSemaphore.flag = False
