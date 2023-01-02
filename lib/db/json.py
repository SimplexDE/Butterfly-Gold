import json




def read_file(file):
	with open(file) as f:
		return json.load(f)




class JSONDB:
	def __init__(self):
		self.data = read_file


	def get_data(self, identification):
		return self.data[str(identification)]
