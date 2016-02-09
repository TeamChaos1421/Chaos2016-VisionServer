import time

import KernelThread
import StreamServer
import ColorKernel
import AutoAim

# Camera URI
camera = 'http://freshfoodslivecam.usm.edu/axis-cgi/mjpg/video.cgi?fake=video.mjpg'

# Semaphores
goalChannel = StreamServer.DataSemaphore()
ballChannel = StreamServer.DataSemaphore()
autoAimChannel = StreamServer.DataSemaphore()

# Kernels
kernels = [
	ColorKernel.ColorKernelInteractive("Goal: ", goalChannel),
	ColorKernel.ColorKernelInteractive("Ball: ", ballChannel),
]

########################################################################
########################################################################
########################################################################

# Run All of The Computer Vision Parts Here
kernelThread = KernelThread.KernelThread(camera, kernels)
kernelThread.start()

# Run AutoAim Here
autoAim = AutoAim.AutoAim(autoAimChannel, goalChannel)
autoAim.start()

# Listen for Requests from the RoboRIO Here
streamServer = StreamServer.StreamServer(5800, autoAimChannel)
streamServer.start()
