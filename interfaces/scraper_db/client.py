from pymongo import MongoClient
from config import MAIN_NODE_IP


CLIENT = MongoClient(f'mongodb://{MAIN_NODE_IP}:27017/')

def get_db():
    return CLIENT['scraper_v3']

