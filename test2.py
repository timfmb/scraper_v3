from pymongo import MongoClient
from config import MAIN_NODE_IP
from interfaces.scraper_db.websites.service import get_all_names


client = MongoClient(f"mongodb://{MAIN_NODE_IP}:27017")

db = client["scraping_data"]
validation_cache_collection = db["validation_cache"]

new_scraper_db = client["scraper_v3"]
new_scraper_collection = new_scraper_db["websites"]


all_names = get_all_names()

validation_cache_results = validation_cache_collection.find({})

for result in validation_cache_results:
    if result['broker_name'] in all_names:
        print(result['broker_name'], result['total_listings'], result['error_counts'])
        new_scraper_collection.update_one({'name': result['broker_name']}, {'$set': {'last_listing_count': result['total_listings'], 'last_error_counts': result['error_counts']}})
    

