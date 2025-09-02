from applications.list_page_scraper.base_scrapers.base_playwright_scraper import BasePlaywrightScraper
from playwright.async_api import async_playwright
from typing import Callable
from bs4 import BeautifulSoup
from time import sleep
import asyncio
from interfaces.scraper_db.pages.service import create_page, set_list_page_data, remove_pages


class MultiPageButtonClickPlaywrightScraper(BasePlaywrightScraper):
    def __init__(
        self,
        website_name: str
    ):
        super().__init__(website_name)

    async def run_url_string(self, url_string):
        url = f'{self.website.url}/{url_string}'
        used_urls = set()
        urls = set()
        browser = None
        page = None
        context = None

        async with async_playwright() as p:
            try:
                browser = await self.launch_browser(p)
                page, context = await self.new_page(browser)
                page = await self.load_page(page, url)
                if not page:  # Check if page load was successful
                    return urls

                await asyncio.sleep(5)

                if self.website.list_page_config.pre_scrape_function:
                    await self._execute_string_function_pw_page(self.website.list_page_config.pre_scrape_function, page)

                last_url_count = 0

                while not page.is_closed():
                    try:
                        await asyncio.sleep(8)
                                            
                        try:
                            html = await page.content()
                            soup = BeautifulSoup(html, 'html.parser')
                            page_urls = self._execute_string_function(self.website.list_page_config.scraping_function, soup)
                            
                            for scraped_url in page_urls:
                                if scraped_url not in used_urls:
                                    create_page(self.website.name, scraped_url)
                                    used_urls.add(scraped_url)
                                    urls.add(scraped_url)

                            if self.website.list_page_config.extra_data_function:
                                extra_data = self._execute_string_function(self.website.list_page_config.extra_data_function, soup)
                                for url, data in extra_data.items():
                                    try:
                                        set_list_page_data(url, data)
                                    except Exception as e:
                                        pass

                            else:
                                for url in page_urls:
                                    set_list_page_data(url, {})
                            
                            if len(urls) == last_url_count:
                                break

                            last_url_count = len(urls)

                            if not page.is_closed():
                                try:
                                    await page.locator(self.website.list_page_config.button_selector).first.click()
                                    await asyncio.sleep(5)
                                except Exception as e:
                                    print(e)
                                try:
                                    await page.wait_for_load_state('networkidle', timeout=self.timeout)
                                except Exception as e:
                                    pass

                        except Exception as e:
                            print(e)
                            break
                    except Exception as e:
                        print(e)
                        break

            except Exception as e:
                print(e)
                pass
            finally:
                await self.safe_close(browser, context, page)

        return urls


    def run(self):
        print(f'Running URL Scraper: {self.website.name}')

        agg_urls = set()
        for url_string in self.website.list_page_config.url_strings:
            try:
                urls = asyncio.run(self.run_url_string(url_string))
                agg_urls.update(urls)
            except Exception as e:
                print(e)
                continue
        
        remove_pages(self.website.name, list(agg_urls))
        print(f'{self.website.name}: Scraped {len(agg_urls)} urls')
        return self.website.name, len(agg_urls)
