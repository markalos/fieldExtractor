from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['name_of_database']

class DBManager():
	def __init__(self, *, dbName : str, collection : str, host : str, port : int):
		
		self.dbName = dbName
		self.host = host
		self.port = port

		self.client = MongoClient(host, port)
		self.db = self.client[dbName]
		self.collection = self.db[collection]

	def insertMany(self, records):
		# self.collection.insert_many(records)
		for record in records:
			self.collection.insert(record)



