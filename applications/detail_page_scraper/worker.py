from playwright.async_api import async_playwright
from time import time
from random import choice, randint
import asyncio
from applications.detail_page_scraper.priority_queue import PriorityQueue
from interfaces.webshare_client import WebshareClient
from interfaces.scraper_db.pages.service import set_page_html, remove_page
import traceback

class ScraperWorker:
    def __init__(self, url_queue: PriorityQueue):
        self.webshare_client = WebshareClient()
        self.proxy_list = self.webshare_client.list_proxies()
        self.url_queue = url_queue

        
    async def scrape_page(self, page, url_dict: dict):
        try:
            print(f'Scraping {url_dict["url"]}')
            page_config = url_dict['config']
            if page_config.get('wait_until'):
                wait_until = page_config['wait_until']
            else:
                wait_until = 'domcontentloaded'

            response = await page.goto(
                url_dict['url'], 
                timeout=90000,
                wait_until=wait_until
            )

            if page_config.get('wait_for_selector'):
                await page.locator(page_config['wait_for_selector']).first.wait_for(state='attached', timeout=45000)

            print(f'{url_dict["url"]} - {response.status}')
            
            if response.status == 404:
                remove_page(url_dict['url'])
                self.url_queue.remove_from_processing(url_dict)
                return False
            
            if response.status != 200:
                current_priority = url_dict['priority']
                url_dict.pop('priority')
                url_dict['retry_time'] = time() + 300 * current_priority
                self.url_queue.put(url_dict, min(current_priority + 1, 9), force=True)  # Cap at max priority
                return False
            
            html = await page.content()
            set_page_html(url_dict['url'], html)
            self.url_queue.remove_from_processing(url_dict)
            return True
        except Exception as e:
            print("Error in ScraperWorker page scrape: ", e)
            traceback.print_exc()
            current_priority = url_dict['priority']
            url_dict.pop('priority')
            url_dict['retry_time'] = time() + 300 * current_priority
            self.url_queue.put(url_dict, min(current_priority + 1, 9), force=True)  # Cap at max priority
            return False
        finally:
            await page.close()




    async def run(self):
        async with async_playwright() as p:
            while True:
                try:
                    if self.url_queue.empty():
                        await asyncio.sleep(5)
                        continue
                    
                    proxy = choice(self.proxy_list)
                    browser = await p.chromium.launch(proxy=proxy, args=['--no-sandbox', '--disable-setuid-sandbox'], headless=True)
                    
                    for _ in range(4):
                        context = await browser.new_context(
                            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        )

                        tasks = []
                        for _ in range(randint(4, 8)):
                            if self.url_queue.empty():
                                break

                            url_dict, priority = self.url_queue.get()
                            self.url_queue.set_in_processing(url_dict)
                            if 'retry_time' in url_dict and time() < url_dict['retry_time']:
                                self.url_queue.put(url_dict, priority, force=True)
                                continue

                            url_dict['priority'] = priority
                            page = await context.new_page()
                            tasks.append(asyncio.create_task(self.scrape_page(page, url_dict)))

                        # Wait for all 10 tasks to finish
                        await asyncio.gather(*tasks)
                        await context.close()

                    await browser.close()
                except Exception as e:
                    print("Error in ScraperWorker: ", e)
                    await asyncio.sleep(1)

