class Alarm():

	def __init__(self,logger):
		self.logger = logger

	def execute(self,message,request,exception):
		self.logger.exception(exception)