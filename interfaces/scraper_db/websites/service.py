from ..client import get_db
from .models import Website
from datetime import datetime, timedelta
import random
from interfaces.scraper_db.pages.service import count_pages_for_website
from typing import Literal


def get_collection():
    db = get_db()
    return db['websites']



def get_website_by_name(name: str) -> Website | None:
    collection = get_collection()
    website = collection.find_one({'name': name})
    if website:
        return Website(**website)
    return None


def get_all_websites(run_no_pages: bool = False) -> list[Website]:
    collection = get_collection()
    websites = collection.find()
    if run_no_pages:
        websites = [website for website in websites if count_pages_for_website(website['name'], active=True) == 0]
    return [Website(**website) for website in websites]


def get_website_by_tag(tag: str, run_no_pages: bool = False) -> list[Website]:
    collection = get_collection()
    websites = collection.find({'tags': tag})
    if run_no_pages:
        websites = [website for website in websites if count_pages_for_website(website['name'], active=True) == 0]
    return [Website(**website) for website in websites]



def get_all_tags() -> list[str]:
    collection = get_collection()
    tags = collection.distinct('tags')
    return tags


def get_all_names() -> list[str]:
    collection = get_collection()
    names = collection.distinct('name')
    return names


def get_detail_page_config(website_name: str) -> dict:
    collection = get_collection()
    website = collection.find_one({'name': website_name}, {'detail_page_config': 1})
    if website:
        return website['detail_page_config']
    return None


def update_list_page_scraping_function(website_name: str, function: str):
    print(f"Updating list page scraping function for {website_name} to {function}")
    collection = get_collection()
    collection.update_one({'name': website_name}, {'$set': {'list_page_config.scraping_function': function}})


def update_list_page_extra_data_function(website_name: str, function: str):
    print(f"Updating list page extra data function for {website_name} to {function}")
    collection = get_collection()
    if function.strip() == '':
        function = None
    collection.update_one({'name': website_name}, {'$set': {'list_page_config.extra_data_function': function}})


def update_list_page_pre_scrape_function(website_name: str, function: str):
    print(f"Updating list page pre scrape function for {website_name} to {function}")
    collection = get_collection()
    if function.strip() == '':
        function = None
    collection.update_one({'name': website_name}, {'$set': {'list_page_config.pre_scrape_function': function}})


def update_detail_page_scraper_string(website_name: str, scraper_string: str):
    collection = get_collection()
    collection.update_one({'name': website_name}, {'$set': {'detail_page_config.scraper_string': scraper_string}})

def update_list_page_config_settings(
    website_name: str, 
    wait_type: Literal['load state'],
    wait_for: Literal['domcontentloaded', 'networkidle'],
    use_route_intercept: bool,
    browser_type: Literal['chromium', 'firefox'],
    use_proxy: bool,
    bypass_cloudflare: bool,
    url_strings: list[str],
    timeout: int = 90000,
    page_start: int|None = None,
    page_step: int|None = None,
    max_retries: int|None = None,
    max_pages: int|None = None
):
    print(f"Updating list page config settings for {website_name}")
    collection = get_collection()
    collection.update_one({'name': website_name}, {'$set': 
        {
            'list_page_config.wait_type': wait_type,
            'list_page_config.wait_for': wait_for,
            'list_page_config.use_route_intercept': use_route_intercept,
            'list_page_config.browser_type': browser_type,
            'list_page_config.use_proxy': use_proxy,
            'list_page_config.bypass_cloudflare': bypass_cloudflare,
            'list_page_config.url_strings': url_strings,
            'list_page_config.timeout': timeout,
            'list_page_config.page_start': page_start,
            'list_page_config.page_step': page_step,
            'list_page_config.max_retries': max_retries,
            'list_page_config.max_pages': max_pages
        }})
    

def update_detail_page_config_settings(
    website_name: str,
    wait_until: Literal['load', 'domcontentloaded', 'networkidle'],
    wait_for_selector: str|None = None
):
    print(f"Updating detail page config settings for {website_name}")
    collection = get_collection()
    collection.update_one({'name': website_name}, {'$set': 
        {
            'detail_page_config.wait_until': wait_until,
            'detail_page_config.wait_for_selector': wait_for_selector
        }})


def handle_upload(
    website_name: str,
    new_listing_count: int,
    new_error_counts: dict
):
    collection = get_collection()
    collection.update_one({'name': website_name}, {'$set': 
        {
            'last_listing_count': new_listing_count,
            'last_error_counts': new_error_counts,
            'last_scrape_valid': True,
            'last_upload_date': datetime.now()
        }})


def update_defaults(website_name: str, location: str|None = None, country: str|None = None, currency: str|None = None):
    collection = get_collection()
    collection.update_one({'name': website_name}, {'$set': 
        {
            'detail_page_config.defaults.location': location,
            'detail_page_config.defaults.country': country,
            'detail_page_config.defaults.currency': currency
        }})
    
    
