def get_errors():
	return ErrorBox.get_instance().get_errors()

class ErrorBox(object):

	instance = None

	@classmethod
	def get_instance(cls):
		if not cls.instance:
			cls.instance = cls()
		return cls.instance

	def __init__(self):
		self.errors = []

	def get_errors(self):
		errors = self.errors
		self.errors = []
		return errors

	def add_error(self, error):
		self.errors.append(error)