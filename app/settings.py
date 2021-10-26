import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
ADMIN_LIST = os.getenv('ADMINS_LIST').split(':')

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')

MENU_DELIMITER = '——'
DATE_FORMAT = '%d.%m.%Y'
