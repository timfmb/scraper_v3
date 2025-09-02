from pymongo import MongoClient
from config import MAIN_NODE_IP
from refactor_scrapers import extract_url_extractor_multi_page_playwright, extract_data_extractor
from interfaces.scraper_db.websites.builder import ScraperBuilder
from interfaces.scraper_db.websites.service import get_all_names


client = MongoClient(f"mongodb://{MAIN_NODE_IP}:27017")

db = client["scraping_data"]
upload_collection = db["upload_config"]
scrapers_collection = db["scrapers"]

new_scraper_db = client["scraper_v3"]
new_scraper_collection = new_scraper_db["websites"]


upload_config = upload_collection.find_one({})
boatseekr_sites = upload_config["Boatseekr"]

current_scrapers = [i['name'] for i in new_scraper_collection.find({})]
print(current_scrapers)


for site in boatseekr_sites:
    if site in current_scrapers:
        continue

    scraper = scrapers_collection.find_one({"name": site})
    if not scraper:
        print(f"Scraper not found for {site}")
        continue

    if "from applications.url_extractor.extractor.url_scrapers.multi_page_simple_scraper import MultiPageSimpleScraper" not in scraper['url_extractor_code']:
        continue

    if "new_generic_scraper" not in scraper['code']:
        continue

    print(site)



    extracted_url_extractor = extract_url_extractor_multi_page_playwright(scraper['url_extractor_code'])
    extracted_data_extractor = extract_data_extractor(scraper['code'])


    builder = ScraperBuilder()
    builder.create_website(url=extracted_url_extractor['base_url'], name=site, tags=[scraper['type']])
    builder.create_multi_page_playwright_config(
        url_strings=extracted_url_extractor['url_strings'],
        scraping_function=extracted_url_extractor['scraping_function'],
        extra_data_function=extracted_url_extractor['extra_data_function'],
        page_start=extracted_url_extractor['page_start'],
        page_step=extracted_url_extractor['page_step']
    )
    builder.create_detail_page_config(scraper_string=extracted_data_extractor['class_definition'])
    builder.save()






















