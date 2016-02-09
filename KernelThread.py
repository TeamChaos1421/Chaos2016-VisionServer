#!/usr/bin/python

import threading
import numpy as np
import cv2

# OpenCV Kernel Thread Class Definition
class KernelThread (threading.Thread):
	
	def __init__(self, uri, kernels):
		threading.Thread.__init__(self)
		self.uri = uri
		self.kernels = kernels
	
	def run(self):
		# Open the Camera Stream
		cam = cv2.VideoCapture(self.uri)
		
		# Initialize Vision Kernels
		for kernel in self.kernels:
			kernel.init()
		
		while(1):
			# Get Image from Camera
			if(cam.isOpened()):
				ret, image = cam.read()
			
			# Run Vision Kernels
			for kernel in self.kernels:
				kernel.run(image)
		
			# Check Escape Key
			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				break
