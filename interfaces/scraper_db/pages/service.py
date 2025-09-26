from ..client import get_db
from .models import Page
from datetime import datetime, timedelta
import random
from logging_config import get_logger

logger = get_logger(__name__)

def get_collection():
    db = get_db()
    return db['pages']


def get_websites_collection():
    db = get_db()
    return db['websites']


def get_pages_for_website(website_name: str, active: bool = None) -> list[Page]:
    collection = get_collection()
    filter = {'website_name': website_name}
    if active is not None:
        filter['active'] = active
    pages = collection.find(filter)
    return [Page(**page) for page in pages]


def count_pages_for_website(website_name: str, active: bool = None) -> int:
    collection = get_collection()
    filter = {'website_name': website_name}
    if active is not None:
        filter['active'] = active
    return collection.count_documents(filter)


def get_active_page_urls_for_website(website_name: str) -> list[str]:
    collection = get_collection()
    pages = collection.find({'website_name': website_name, 'active': True}, {'url': 1})
    return [page['url'] for page in pages]



def get_active_page_errors_for_website(website_name: str) -> list[dict]:
    collection = get_collection()
    pages = collection.find({'website_name': website_name, 'active': True}, {'errors': 1})
    return [page['errors'] for page in pages if page and page.get('errors')]


def get_active_page_error_counts_for_website(website_name: str) -> list[dict]:
    errors = get_active_page_errors_for_website(website_name)
    error_counts = {}
    for error in errors:
        for error_type in error:
            if error_type in error_counts:
                error_counts[error_type] += 1
            else:
                error_counts[error_type] = 1
    return error_counts


def create_page(website_name: str, url: str) -> None:
    if not url.startswith('http'):
        return None
    collection = get_collection()
    #check if a page exists with the same url
    existing_page = collection.find_one({'url': url})
    if existing_page:
        # If page exists but is inactive, reactivate it
        collection.update_one(
            {'url': url},
            {'$set': {'active': True}}
        )
        return
    
    page = Page(url=url, website_name=website_name)
    
    collection.insert_one(page.model_dump())


def remove_page(url: str) -> None:
    collection = get_collection()
    collection.update_one(
        {'url': url},
        {'$set': {'active': False}}
    )


def remove_pages(website_name: str, urls_to_keep: list[str]) -> None:
    collection = get_collection()
    collection.update_many(
        {'website_name': website_name, 'url': {'$nin': urls_to_keep}},
        {'$set': {'active': False}}
    )



def set_list_page_data(url: str, data: dict|None) -> None:
    if data is None:
        data = {}
    data['url'] = url
    collection = get_collection()
    collection.update_one(
        {'url': url}, 
        {'$set': {'list_page_data': data}}
    )


def get_detail_page_config(website_name: str) -> dict:
    collection = get_websites_collection()
    website = collection.find_one({'name': website_name}, {'detail_page_config': 1})
    if website:
        return website['detail_page_config']
    return None


def get_detail_pages_wo_html_to_download() -> list[dict]:
    collection = get_collection()
    pages = collection.find({'html': None, 'active': True}, {'url': 1, 'website_name': 1})
    configs = {}
    built_pages = []
    for page in pages:
        if page['website_name'] not in configs:
            configs[page['website_name']] = get_detail_page_config(page['website_name'])
        page['config'] = configs[page['website_name']]
        built_pages.append(page)
    random.shuffle(built_pages)
    return built_pages
    

def get_detail_pages_to_redownload() -> list[dict]:
    collection = get_collection()
    # Random cutoff time between 18 and 36 hours
    random_hours = random.uniform(36, 48)
    cutoff_time = datetime.now() - timedelta(hours=random_hours)

    logger.info(f'Cutoff time: {cutoff_time}')
    
    pages = collection.find({'active': True, 'last_scraped': {'$lt': cutoff_time}}, {'url': 1, 'website_name': 1})
    configs = {}
    built_pages = []
    for page in pages:
        if page['website_name'] not in configs:
            configs[page['website_name']] = get_detail_page_config(page['website_name'])
        page['config'] = configs[page['website_name']]
        built_pages.append(page)
    random.shuffle(built_pages)
    return built_pages


def set_page_html(url: str, html: str) -> None:
    collection = get_collection()
    collection.update_one(
        {'url': url},
        {'$set': {
            'html': html,
            'last_scraped': datetime.now()
        }}
    )


def set_page_extracted_data(url: str, extracted_data: dict) -> None:
    collection = get_collection()
    collection.update_one(
        {'url': url},
        {'$set': {
            'extracted_data': extracted_data
        }}
    )


def set_page_errors(url: str, errors: list[str]) -> None:
    collection = get_collection()
    collection.update_one(
        {'url': url},
        {'$set': {
            'errors': errors
        }}
    )


def get_page_errors(url: str) -> list[str]:
    collection = get_collection()
    page = collection.find_one({'url': url}, {'errors': 1})
    if page:
        return page['errors']
    return []




def set_page_hash(url: str, hash: str) -> None:
    collection = get_collection()
    collection.update_one(
        {'url': url},
        {'$set': {
            'hash': hash
        }}
    )


def delete_all_html_for_website(website_name: str) -> None:
    collection = get_collection()
    collection.update_many(
        {'website_name': website_name},
        {'$unset': {'html': ''}}
    )



def get_inferred_description(url: str) -> dict:
    """
    Get cached inferred description for a URL.
    
    Returns:
        dict: Cached description data or None if not found
    """
    try:
        collection = get_collection()
        page = collection.find_one({'url': url}, {'extracted_data.inferred_description': 1})
        if page and page.get('extracted_data') and page['extracted_data'].get('inferred_description'):
            return page['extracted_data']['inferred_description']
        return None
    except Exception as e:
        logger.info(f"Error retrieving inferred description for URL {url}: {e}")
        return None


def set_inferred_description(url: str, description: str, original_description_hash: str) -> None:
    """
    Cache inferred description for a URL with improved error handling and upsert logic.
    
    Args:
        url: The page URL
        description: The cleaned description
        original_description_hash: Hash of the original description
    """
    try:
        collection = get_collection()
        
        # Use upsert to handle cases where the page doesn't exist yet
        result = collection.update_one(
            {'url': url},
            {
                '$set': {
                    'extracted_data.inferred_description': {
                        'description': description, 
                        'original_description_hash': original_description_hash
                    }
                }
            },
            upsert=True  # Create document if it doesn't exist
        )
        
        # Log the result for debugging
        if result.upserted_id:
            logger.info(f"Created new page document for URL: {url}")
        elif result.modified_count > 0:
            logger.info(f"Updated inferred description cache for URL: {url}")
        else:
            logger.info(f"No changes made to cache for URL: {url}")
            
    except Exception as e:
        logger.info(f"Error setting inferred description for URL {url}: {e}")
        raise

