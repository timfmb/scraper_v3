from pymongo import MongoClient
import json
from dotenv import load_dotenv
import os

load_dotenv()

ATLAS_CLIENT = MongoClient(os.getenv('ATLAS_DB_URI'))

def get_atlas_search_engine_db():
    db = ATLAS_CLIENT['search-engine']
    return db

