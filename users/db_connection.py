import pymongo
import certifi
from dotenv import load_dotenv
import os

url = os.getenv('MONGO_URL')

# client = pymongo.MongoClient(url)
client = pymongo.MongoClient(url, tlsCAFile=certifi.where())

db = client['girman']

