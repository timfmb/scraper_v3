from bs4 import BeautifulSoup
from applications.data_extractor.base_scraper import BaseScraper
from typing import Literal
from interfaces.scraper_db.websites.service import get_all_websites, get_website_by_tag, get_website_by_name
from interfaces.scraper_db.pages.service import get_pages_for_website
import time
from interfaces.monitoring import MonitoringManager
from datetime import datetime
import questionary
from applications.data_extractor.scraping_utilities.clean import remove_all_html_attributes
from applications.data_extractor.scraping_utilities.location import extract_country
from applications.data_extractor.scraping_utilities.dimensions import feet_inches_to_meters, meters_to_meters, feet_only_to_meters, decimal_feet_to_meters, decimal_feet_contracted_to_meters, feet_inches_dot_to_meters, extract_float_from_european_number, ft_to_metres, feet_inches_to_meters2, slash_separated_to_meters, identify_and_extract_boat_length_format
from applications.data_extractor.scraping_utilities.extra import extract_fuel_tank_size, extract_engine_manufacturer
from applications.data_extractor.scraping_utilities.price import extract_price_by_removing_non_numeric, extract_price_and_currency
from unidecode import unidecode
from interfaces.scraper_db.websites.models import Website
from concurrent.futures import ProcessPoolExecutor
from logging_config import get_logger

logger = get_logger(__name__)


def execute_string_scraper(scraper_string: str):
    """Execute a string function with soup as parameter"""
    exec_globals = {
        'BeautifulSoup': BeautifulSoup,
        'BaseScraper': BaseScraper,
        '__builtins__': __builtins__,
        'remove_all_html_attributes': remove_all_html_attributes,
        'extract_country': extract_country,
        'feet_inches_to_meters': feet_inches_to_meters,
        'meters_to_meters': meters_to_meters,
        'feet_only_to_meters': feet_only_to_meters,
        'decimal_feet_to_meters': decimal_feet_to_meters,
        'decimal_feet_contracted_to_meters': decimal_feet_contracted_to_meters,
        'feet_inches_dot_to_meters': feet_inches_dot_to_meters,
        'extract_float_from_european_number': extract_float_from_european_number,
        'ft_to_metres': ft_to_metres,
        'feet_inches_to_meters2': feet_inches_to_meters2,
        'slash_separated_to_meters': slash_separated_to_meters,
        'identify_and_extract_boat_length_format': identify_and_extract_boat_length_format,
        'extract_fuel_tank_size': extract_fuel_tank_size,
        'extract_engine_manufacturer': extract_engine_manufacturer,
        'extract_price_by_removing_non_numeric': extract_price_by_removing_non_numeric,
        'extract_price_and_currency': extract_price_and_currency,
        'unidecode': unidecode,
    }
    
    # Keep track of what was in the namespace before execution
    original_keys = set(exec_globals.keys())
    
    # Execute the function string to define it in the namespace
    exec(scraper_string, exec_globals)        
    # Find new classes that were added by the exec
    new_classes = []
    for name in exec_globals.keys():
        if (name not in original_keys and 
            callable(exec_globals[name]) and 
            not name.startswith('_')):
            new_classes.append(name)
            
    if new_classes:
        scraper_class = exec_globals[new_classes[0]]
        result = scraper_class()
        return result
    else:
        raise ValueError("No callable function found in the function string")
    


def run_website(website: Website, full_scrape: bool, monitoring_manager: MonitoringManager):
    try:
        monitoring_manager.add_data_extraction_real_time(website.name, datetime.now())
        if not website.detail_page_config:
            logger.warning(f'No detail page config found for {website.name}')
            return
        logger.info(f'Extracting data for {website.name}')
        scraper = execute_string_scraper(website.detail_page_config.scraper_string)
        scraper.run(full_scrape=full_scrape)
    except Exception as e:
        logger.error(e)
        return



def run(
    run_type: Literal['all', 'tag', 'name'], 
    tag: str | None = None, 
    name: str | None = None,
    continuous: bool = False
):
    if run_type == 'all':
        websites = get_all_websites()
    elif run_type == 'tag':
        websites = get_website_by_tag(tag)
    elif run_type == 'name':
        website = get_website_by_name(name)
        if website:
            websites = [website]
        else:
            logger.error(f'Website {name} not found')

    monitoring_manager = MonitoringManager()

    if run_type != 'name':
        if questionary.confirm('Only scrape New Websites?').ask():
            new_websites = []
            for website in websites:
                if all(p.extracted_data == None for p in get_pages_for_website(website.name, active=True)):
                    new_websites.append(website)
            websites = new_websites


        if questionary.confirm('Run only invalid websites?').ask():
            websites_to_run = []
            for website in websites:
                if not website.last_scrape_valid:
                    websites_to_run.append(website)
            websites = websites_to_run


    if questionary.confirm('Use Cached data?').ask():
        full_scrape = False
    else:
        full_scrape = True

    num_workers = int(questionary.text('Number of workers').ask())

    while True:
        monitoring_manager.set_data_extraction_sleeping(False)
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            executor.map(run_website, websites, [full_scrape] * len(websites), [monitoring_manager] * len(websites))
        if not continuous:
            break
        logger.info('Sleeping for 12 hours')
        monitoring_manager.set_data_extraction_sleeping(True)
        time.sleep(86400/2)