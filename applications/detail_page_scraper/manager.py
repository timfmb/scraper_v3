from applications.detail_page_scraper.priority_queue import PriorityQueue
from interfaces.scraper_db.pages.service import get_detail_pages_wo_html_to_download, get_detail_pages_to_redownload
import time
from applications.detail_page_scraper.worker import ScraperWorker
from threading import Thread
import asyncio


class DetailPageScraperManager:
    def __init__(self):
        self.queue = PriorityQueue()


    def run_queue_producer(self):
        print("producer started")
        while True:
            urls = get_detail_pages_wo_html_to_download()
            if urls:
                added_count = 0
                for url_dict in urls:
                    if self.queue.put(url_dict, 0):
                        added_count += 1
                if added_count > 0:
                    print(f'Added {added_count} new pages to queue')
            else:
                urls = get_detail_pages_to_redownload()
                if urls:
                    added_count = 0
                    for url_dict in urls:
                        if self.queue.put(url_dict, 1):
                            added_count += 1
                    if added_count > 0:
                        print(f'Added {added_count} pages to queue to redownload')
                else:
                    print('No pages to redownload')
            time.sleep(10)


    async def run_queue_consumer(self):
        print("consumer started")
        worker = ScraperWorker(self.queue)
        await worker.run()


    def run(self):
        print('Starting detail page scraper manager')
        thread = Thread(target=self.run_queue_producer)
        thread.start()
        print('Starting detail page scraper consumer')
        asyncio.run(self.run_queue_consumer())
        thread.join()





    


