import threading
import time

class AutoAim (threading.Thread):

	def __init__(self, outChannel, inChannel):
		threading.Thread.__init__(self)
		self.outChannel = outChannel
		self.inChannel = inChannel
	
	def run(self):
		while 1:
			
			# Wait for Data to be Requested
			while not self.outChannel.flag:
				time.sleep(0.01)
			
			# Request Data
			self.inChannel.flag = True
			while self.inChannel.flag:
				time.sleep(0.01)
			
			# Setup Environment for WIP
			global_vars = {}
			local_vars = {"data": self.inChannel.data, "request": self.outChannel.data}
			
			# Run Separate File While Testing
			with open("AutoAimWIP.py") as f:
				code = compile(f.read(), "AutoAimWIP.py", 'exec')
				try:
					exec(code, global_vars, local_vars)
				except:
					print("AutoAimWIP.py is currently broken!")
					local_vars["output"] = "0 0"
			
			# Send Data to Server
			self.outChannel.data = local_vars["output"]
			self.outChannel.flag = False
