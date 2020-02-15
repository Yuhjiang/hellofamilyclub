from pymongo import MongoClient

from .config import MONGODB


db_client = MongoClient(MONGODB['url'])
mongo_db = db_client['hellofamily']
