import datetime,os
class write_log:
	def init(self,log_file):
		if (log_file == False):
			self.log_file == False
		else:
			self.log_file = log_file
	def write(self,log_info):
		if (self.log_file != False):
			self.log_info = log_info
			self.time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
			os.system(f"echo '{self.time}|{self.log_info}' >> {self.log_file}")
		else:
			pass