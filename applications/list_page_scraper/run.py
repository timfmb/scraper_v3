from applications.list_page_scraper.site_type_scrapers.multi_page_playwright_scraper import MultiPagePlaywrightScraper
from applications.list_page_scraper.site_type_scrapers.single_page_playwright_scraper import SinglePagePlaywrightScraper
from applications.list_page_scraper.site_type_scrapers.infinite_scroll_playwright_scraper import InfiniteScrollPlaywrightScraper
from applications.list_page_scraper.site_type_scrapers.button_scroll_playwright_scraper import ButtonScrollPlaywrightScraper
from applications.list_page_scraper.site_type_scrapers.multi_page_button_click_playwright_scraper import MultiPageButtonClickPlaywrightScraper
from interfaces.scraper_db.websites.service import get_all_websites, get_website_by_tag, get_website_by_name
from interfaces.monitoring import MonitoringManager
from datetime import datetime
from typing import Literal
import time
import questionary



def run(
    run_type: Literal['all', 'tag', 'name'],
    tag: str | None = None, 
    name: str | None = None,
    continuous: bool = False
):
    run_no_pages = questionary.confirm("Run only scrapers without pages?").ask()
    manager = MonitoringManager()
    if run_type == 'all':
        websites = get_all_websites(run_no_pages)
    elif run_type == 'tag':
        websites = get_website_by_tag(tag, run_no_pages)
    elif run_type == 'name':
        website = get_website_by_name(name)
        if website:
            websites = [website]
        else:
            print(f'Website {name} not found')
            return

    while True:
        manager.set_list_page_sleeping(False)
        for website in websites:
            manager.add_list_page_real_time(website.name, datetime.now())
            if not website.list_page_config:
                print(f'No list page config found for {website.name}')
                continue

            if website.list_page_scraper_type == 'multi_page_playwright':
                scraper = MultiPagePlaywrightScraper(website_name=website.name)
                scraper.run()
            elif website.list_page_scraper_type == 'single_page_playwright':
                scraper = SinglePagePlaywrightScraper(website_name=website.name)
                scraper.run()
            elif website.list_page_scraper_type == 'infinite_scroll_playwright':
                scraper = InfiniteScrollPlaywrightScraper(website_name=website.name)
                scraper.run()
            elif website.list_page_scraper_type == 'button_scroll_playwright':
                scraper = ButtonScrollPlaywrightScraper(website_name=website.name)
                scraper.run()
            elif website.list_page_scraper_type == 'multi_page_button_click_playwright':
                scraper = MultiPageButtonClickPlaywrightScraper(website_name=website.name)
                scraper.run()
            else:
                print(f'No scraper type found for {website.name}')
        if not continuous:
            break
        manager.set_list_page_sleeping(True)
        print('Sleeping for 12 hours')
        time.sleep(86400/2)

