from applications.list_page_scraper.base_scrapers.base_playwright_scraper import BasePlaywrightScraper
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import asyncio
from interfaces.scraper_db.pages.service import create_page, set_list_page_data, remove_pages
from logging_config import get_logger

logger = get_logger(__name__)


class MultiPagePlaywrightScraper(BasePlaywrightScraper):
    def __init__(
        self,
        website_name: str
    ):
        super().__init__(website_name)


    async def run_page(self, page, url):        
        for attempt in range(self.website.list_page_config.max_retries):
            try:
                if page.is_closed():
                    return set(), {}
                    
                html_page = await self.load_page(page, url)
                if not html_page:  # Check if page load was successful
                    continue
                    
                html = await html_page.content()
                soup = BeautifulSoup(html, 'html.parser')
                new_urls = self._execute_string_function(
                    self.website.list_page_config.scraping_function, soup
                )
                extra_data = {}
                if self.website.list_page_config.extra_data_function:
                    extra_data = self._execute_string_function(
                        self.website.list_page_config.extra_data_function, soup
                    )
                return new_urls, extra_data
            except Exception as e:
                logger.error(f'Error in run_page: {e}')
                await asyncio.sleep(10)
                if attempt == self.website.list_page_config.max_retries - 1:  # Last attempt
                    return set(), {}
        
        return set(), {}
    

    async def run_url_string(self, browser, url_string):
        unformatted_url = f'{self.website.url}/{url_string}'
        urls = set()
        last_count = 0
        current_page = self.website.list_page_config.page_start
        page = None
        context = None
        
        try:
            page, context = await self.new_page(browser)
            while True:
                try:
                    url = unformatted_url.format(current_page)
                    new_urls, extra_data = await self.run_page(page, url)

                    for url in new_urls:
                        create_page(self.website.name, url)
                    for url, data in extra_data.items():
                        set_list_page_data(url, data)

                    urls.update(new_urls)

                    if len(urls) == last_count or (self.website.list_page_config.max_pages and current_page >= self.website.list_page_config.max_pages):
                        break

                    last_count = len(urls)
                    current_page += self.website.list_page_config.page_step
                except Exception as e:
                    break
        finally:
            if page and context:
                await self.safe_close(None, context, page)

        return list(urls)

    async def run_scraper(self):
        async with async_playwright() as p:
            browser = None
            try:
                browser = await self.launch_browser(p)
                agg_urls = set()
                for url_string in self.website.list_page_config.url_strings:
                    urls = await self.run_url_string(browser, url_string)
                    agg_urls.update(urls)
               
                return self.website.name, agg_urls
            finally:
                if browser:
                    await self.safe_close(browser)


    def run(self):
        logger.info(f'Running URL Scraper: {self.website.name}')

        website_name, agg_urls = asyncio.run(self.run_scraper())
        remove_pages(
            self.website.name, 
            urls_to_keep=list(agg_urls)
        )
        logger.info(f'{self.website.name}: Scraped {len(agg_urls)} urls')
        return website_name, len(agg_urls)