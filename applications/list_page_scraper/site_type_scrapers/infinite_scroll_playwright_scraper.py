from applications.list_page_scraper.base_scrapers.base_playwright_scraper import BasePlaywrightScraper
from playwright.async_api import async_playwright
from typing import Callable
from bs4 import BeautifulSoup
from time import sleep
import asyncio
from interfaces.scraper_db.pages.service import create_page, set_list_page_data, remove_pages




class InfiniteScrollPlaywrightScraper(BasePlaywrightScraper):
    def __init__(
        self,
        website_name: str,
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
                if not page:
                    return urls

                await asyncio.sleep(5)

                if self.website.list_page_config.pre_scrape_function:
                    await self._execute_string_function_pw_page(self.website.list_page_config.pre_scrape_function, page)

                page_height = await page.evaluate('document.body.scrollHeight')
                scrolls = 0

                while not page.is_closed():
                    try:
                        await asyncio.sleep(10)
                        for i in range(200):
                            await page.mouse.wheel(0, page_height/200)
                            await asyncio.sleep(0.05)
                        for i in range(20):
                            await page.mouse.wheel(0, -page_height/200)
                            await asyncio.sleep(0.05)
                        for i in range(20):
                            await page.mouse.wheel(0, page_height/200)
                            await asyncio.sleep(0.05)
                            
                        await asyncio.sleep(10)
                        try:
                            await page.wait_for_load_state('networkidle', timeout=60000)
                        except Exception as e:
                            pass
                        new_page_height = await page.evaluate('document.body.scrollHeight')

                        if new_page_height == page_height:
                            break

                        page_height = new_page_height

                        scrolls += 1
                        if self.website.list_page_config.max_scrolls and scrolls >= self.website.list_page_config.max_scrolls:
                            break

                        try:
                            html = await page.content()
                            soup = BeautifulSoup(html, 'html.parser')
                            urls = set(self._execute_string_function(self.website.list_page_config.scraping_function, soup))
                            for scraped_url in urls:
                                if scraped_url not in used_urls:
                                    create_page(self.website.name, scraped_url)
                                    used_urls.add(scraped_url)

                        except Exception as e:
                            pass

                    except Exception as e:
                        break

                # Final scrape
                if not page.is_closed():
                    try:
                        html = await page.content()
                        soup = BeautifulSoup(html, 'html.parser')
                        urls = set(self._execute_string_function(self.website.list_page_config.scraping_function, soup))
                        for scraped_url in urls:
                            if scraped_url not in used_urls:
                                create_page(self.website.name, scraped_url)
                                used_urls.add(scraped_url)

                        if self.website.list_page_config.extra_data_function:
                            extra_data = self._execute_string_function(self.website.list_page_config.extra_data_function, soup)
                            for url, data in extra_data.items():
                                try:
                                    set_list_page_data(url, data)
                                    pass
                                except Exception as e:
                                    pass

                        else:
                            for url in urls:
                                set_list_page_data(url, {})

                    except Exception as e:
                        pass

            except Exception as e:
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
                continue
        
        remove_pages(self.website.name, list(agg_urls))
        print(f'{self.website.name}: Scraped {len(agg_urls)} urls')
        return self.website.name, len(agg_urls)
