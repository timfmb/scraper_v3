import requests
from diskcache import Cache
import traceback
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from interfaces.scraper_db.client import get_db



class MongoLocalImageUrlCache:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['image_cache']

    def set(self, url, image_url):
        self.collection.delete_many({'url': url})
        self.collection.insert_one({'url': url, 'image_url': image_url})

    def get(self, url):
        result = self.collection.find_one({'url': url}, {'image_url': 1})
        if result:
            return result['image_url']
        else:
            return None



class ImageManager:
    def __init__(self):
        self.cache_url = f'http://104.248.99.69'
        self.local_cache = MongoLocalImageUrlCache()
        

    def check_local_cache(self, url):
        local_cache_check = self.local_cache.get(url)
        if local_cache_check is not None:
            return local_cache_check
        else:
            return None
        


    def get_or_add_to_cache(self, urls):
        try:
            r = requests.post(f'{self.cache_url}/client/get-urls-or-add-to-queue', json={'urls': urls})
            result = r.json()
            successful = {}
            added_to_queue = []

            for url, url_result in result['urls'].items():
                if url_result['spaces_url']:
                    successful[url] = url_result['spaces_url']
                else:
                    added_to_queue.append(url)
            
            return successful, added_to_queue
        except:
            return {}, []


    
    def poll_for_cache_result(self, url):
        try:
            sleep(5)
            for i in range(5):
                sleep(5)
                params = {'url': url}
                r = requests.get(f'{self.cache_url}/client/get-url', params=params, timeout=60)

                if r.status_code == 200 and r.json()['url'] is not None and r.json()['success'] == True:
                
                    self.local_cache.set(url, r.json()['url'])
                    return r.json()['url']
                
                else:
                    continue

            return None
        except:
            traceback.print_exc()
            return None




    def download_images(self, urls):
        try:
            results = []

            not_in_local = []
            for url in urls:
                local_cache_check = self.check_local_cache(url)
                if local_cache_check is None:
                    not_in_local.append(url)
                else:
                    results.append(local_cache_check)
            
            to_poll = []

            if not_in_local:
                successful, added_to_queue = self.get_or_add_to_cache(not_in_local)
                for url in successful:
                    results.append(successful[url])
                    self.local_cache.set(url, successful[url])
                to_poll = added_to_queue

            if to_poll:
                with ThreadPoolExecutor(max_workers=8) as executor:
                    poll_results = executor.map(self.poll_for_cache_result, to_poll)

                for poll_result in poll_results:
                    results.append(poll_result)
            return results
        except:
            traceback.print_exc()
            return None
                

        

        