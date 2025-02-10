import pymongo

url = "mongodb+srv://imrahulkdhyani80:rahul123@cluster0.ftr7u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = pymongo.MongoClient(url)

db = client['girman']

