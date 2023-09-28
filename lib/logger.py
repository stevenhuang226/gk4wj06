class write_log:
	async def __init__(self,log_file):
		if (self.log_file == False):
			self.log_file == False
		else:
			self.log_file = log_file
	async def write(self,log_info):
		if (self.log_file != False):
			self.log_info = log_info
			self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			os.system(f"echo '{self.time}|{self.log_info}' >> {self.log_file}")
		else:
			pass