from bs4 import BeautifulSoup
from applications.data_extractor.base_scraper import BaseScraper
from typing import Literal
from interfaces.scraper_db.websites.service import get_all_websites, get_website_by_tag, get_website_by_name
from interfaces.scraper_db.pages.service import get_pages_for_website
import time
from interfaces.monitoring import MonitoringManager
from datetime import datetime
import questionary

def execute_string_scraper(scraper_string: str):
    """Execute a string function with soup as parameter"""
    exec_globals = {
        'BeautifulSoup': BeautifulSoup,
        'BaseScraper': BaseScraper,
        '__builtins__': __builtins__
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
            print(f'Website {name} not found')

    monitoring_manager = MonitoringManager()

    if questionary.confirm('Only scrape New Websites?').ask():
        new_websites = []
        for website in websites:
            if all(p.extracted_data == None for p in get_pages_for_website(website.name, active=True)):
                new_websites.append(website)
        websites = new_websites


    if questionary.confirm('Use Cached data?').ask():
        full_scrape = False
    else:
        full_scrape = True

    

    while True:
        monitoring_manager.set_data_extraction_sleeping(False)
        for website in websites:
            try:
                monitoring_manager.add_data_extraction_real_time(website.name, datetime.now())
                if not website.detail_page_config:
                    print(f'No detail page config found for {website.name}')
                    continue
                print(f'Extracting data for {website.name}')
                scraper = execute_string_scraper(website.detail_page_config.scraper_string)
                scraper.run(full_scrape=full_scrape)
            except Exception as e:
                print(e)
                continue
        if not continuous:
            break
        print('Sleeping for 12 hours')
        monitoring_manager.set_data_extraction_sleeping(True)
        time.sleep(86400/2)