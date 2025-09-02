from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT = MongoClient(os.getenv('ATLAS_DB_URI'))

def get_db():
    return CLIENT['search-engine']
