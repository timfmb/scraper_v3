from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

IMAGE_DB_CLIENT = MongoClient(os.getenv('IMAGE_DB_URI'))

def get_image_db():
    db = IMAGE_DB_CLIENT['scraping-storage']
    return db