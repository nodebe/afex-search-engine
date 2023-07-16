import os
from pymongo import MongoClient
from dotenv import load_dotenv
from .utils import log_error

load_dotenv()

mongo_username = os.environ.get('MONGO_USERNAME')
mongo_password = os.environ.get('MONGO_PASSWORD')
mongo_host = os.environ.get('MONGO_HOST')
mongo_port = os.environ.get('MONGO_PORT')

connection_count = 1
while connection_count <= 3:
    # Keeps trying to connect on intervals when there is no network.
    try:
        print(f'Trying Connection {connection_count} of 3 times...')
        client = MongoClient(f'mongodb+srv://{mongo_username}:{mongo_password}@{mongo_host}/')
        break
    except Exception as e:
        log_error(file='search/models.py', function='Connect to DB', error=str(e))
        connection_count+=1
        continue

client = MongoClient(f'mongodb+srv://{mongo_username}:{mongo_password}@{mongo_host}/')