import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
ADMIN_LIST = os.getenv('ADMINS_LIST').split(':')

cluster = MongoClient(
    f'mongodb+srv://andersen_lunch_user:{os.getenv("DB_PASS")}@cluster0.mlw8t.mongodb.net/'
    f'{os.getenv("DB_NAME")}?retryWrites=true&w=majority')

db = cluster[os.getenv('DB_NAME')]
collection = db[os.getenv('DB_COLLECTION')]
