from applications.list_page_scraper.base_scrapers.base_playwright_scraper import BasePlaywrightScraper
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio
import traceback
from interfaces.scraper_db.pages.service import create_page, set_list_page_data, remove_pages
from logging_config import get_logger

logger = get_logger(__name__)


class SinglePagePlaywrightScraper(BasePlaywrightScraper):
    def __init__(
        self,
        website_name: str
    ):
        super().__init__(website_name)


    async def run_url_string(self, url_string):
        url = f'{self.website.url}/{url_string}'
        urls = set()
        browser = None

        async with async_playwright() as p:
            try:
                browser = await self.launch_browser(p)
                page, context = await self.new_page(browser)
                page = await self.load_page(page, url)
                if page:
                    html = await page.content()
                    await self.safe_close(browser, context, page)
                    soup = BeautifulSoup(html, 'html.parser')
                    # Execute the scraping function string
                    new_urls = self._execute_string_function(
                        self.website.list_page_config.scraping_function, soup
                    )
                    for url in new_urls:
                        create_page(self.website.name, url)
                    # Execute the extra data function string if it exists
                    if self.website.list_page_config.extra_data_function:
                        extra_data = self._execute_string_function(
                            self.website.list_page_config.extra_data_function, soup
                        )
                        for url, data in extra_data.items():
                            set_list_page_data(url, data)
                    else:
                        for url in new_urls:
                            set_list_page_data(url, {})

                    urls.update(new_urls)

            except Exception as e:
                traceback.print_exc()
                raise
            finally:
                if browser:
                    await self.safe_close(browser, context, page)

        return list(urls)
    

    
    def run(self):
        logger.info(f'Running URL Scraper: {self.website.name}')

        agg_urls = set()
        for url_string in self.website.list_page_config.url_strings:
            try:
                urls = asyncio.run(self.run_url_string(url_string))
                agg_urls.update(urls)
            except Exception as e:
                continue
        
        remove_pages(
            self.website.name, 
            urls_to_keep=list(agg_urls)
        )
        logger.info(f'{self.website.name}: Scraped {len(agg_urls)} urls')
        return self.website.name, len(agg_urls)