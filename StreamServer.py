import threading
import socket
import time

class DataSemaphore:
	flag = False
	data = ""

# Server Thread Class Definition
class StreamThread (threading.Thread):

	def __init__(self, port, connection, address, dataSemaphore):
		threading.Thread.__init__(self)
		self.connection = connection
		self.address = address
		self.port = port
		self.dataSemaphore = dataSemaphore
	
	def run(self):
				
		while 1:
			
			# Get Token Amount Of Data
			data = self.connection.recv(20)
			if not data: break
			
			# Request Data and Wait
			self.dataSemaphore.data = data
			self.dataSemaphore.flag = True
			while self.dataSemaphore.flag:
				time.sleep(0.01)
			
			# Send Data
			self.connection.send(self.dataSemaphore.data+"\n")
		
		# Close Connection When Done
		self.connection.close()

class StreamServer (threading.Thread):
	def __init__(self, port, dataSemaphore):
		threading.Thread.__init__(self)
		self.port = port
		self.dataSemaphore = dataSemaphore
	
	def run(self):
		# Start Listening
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('0.0.0.0', self.port))
		s.listen(1)

		while 1:
			# Create Threads per Connection
			conn, addr = s.accept()
					
			t = StreamThread(self.port, conn, addr, self.dataSemaphore)
			t.start()
