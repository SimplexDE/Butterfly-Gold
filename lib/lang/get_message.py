from ..db.json import JSONDB

db = JSONDB().get_data({})




class GetMessage:
	def __init__(self):
		self.identification = None
		self.message = None


	def get_message(self, identification):
		self.identification = identification
		self.message = self.db.get_data(self.identification)
		return self.message
