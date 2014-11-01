class Alarm():

	def __init__(self,logger):
		self.logger = logger

	def run(self,message,request,exception):
		self.logger.exception(exception)