import settings
from pymongo import MongoClient


client = MongoClient(f'mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}')

db = client[settings.MONGO_DB_NAME]
users = db['users']
menu_collection = db['menu_collection']
