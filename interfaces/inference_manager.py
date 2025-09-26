import asyncio
from diskcache import Cache
from time import sleep
from interfaces.image_db import get_image_db
import requests
import pybase64
import httpx
from interfaces.scraper_db.client import get_db
from config import MAIN_NODE_IP
from interfaces.scraper_db.pages.models import ExtractedData
from logging_config import get_logger

logger = get_logger(__name__)


class MongoInferenceCache:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['inference_cache']


    def set(self, listing_url:str, data:dict):
        self.collection.delete_many({'listing_url': listing_url})
        self.collection.insert_one({
            'listing_url': listing_url,
            'data': data
        })


    def get(self, listing_url:str):
        result = self.collection.find_one({'listing_url': listing_url}, {'data': 1})
        if result:
            return result['data']
        return None
    



class MongoInferenceImageCache:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['inference_image_cache']


    def set(self, listing_url:str, image_content:bytes):
        self.collection.delete_many({'listing_url': listing_url})
        self.collection.insert_one({
            'listing_url': listing_url,
            'image_content': image_content
        })


    def get(self, listing_url:str):
        result = self.collection.find_one({'listing_url': listing_url}, {'image_content': 1})
        if result:
            return result['image_content']
        return None




class InferenceRunner:
    def __init__(self):
        self.image_db = get_image_db()
        self.cache = MongoInferenceCache()
        self.image_cache = MongoInferenceImageCache()


    def check_cache(self, listing_id):
        return self.cache.get(listing_id)
    

    def get_resized_urls(self, image_urls):
        try:
            results = self.image_db['image-data'].find({'original_url': {'$in': image_urls}}, {'original_url':1, 'resized':1, '_id':0})
            resized_urls = []
            used_original_urls = []
            for i in results:
                if i['original_url'] not in used_original_urls and i['resized'] is not None:
                    resized_urls.append(i['resized'])
                    used_original_urls.append(i['original_url'])
            if len(resized_urls) > 0 and len(resized_urls) == len(image_urls):
                return resized_urls
            return None
        except Exception as e:
            logger.info(f'Error: {e}')
            return None
        

    async def download_image(self, client, url, retries=0):
        try:
            cached = self.image_cache.get(url)
            if cached:
                return cached 
            
            r = await client.get(url)
            if r.status_code == 200:
                self.image_cache.set(url, r.content)
                return r.content
            
            return None
        except:
            if retries < 3:
                return await self.download_image(client, url, retries + 1)
            return None
    

    async def download_images(self, image_urls):
        async with httpx.AsyncClient(timeout=120) as client:
            images = await asyncio.gather(*[self.download_image(client, i) for i in image_urls])
            images = [i for i in images if i is not None]
            if len(images) == len(image_urls):
                return images
            return []




    def download_images_for_listing(self, listing:ExtractedData):
        image_urls = listing.image_urls
        resized_urls = self.get_resized_urls(image_urls)
        if resized_urls:
            images = asyncio.run(self.download_images(resized_urls))
            return images
        images = []
        return images
    


    def run_inference_for_listing(self, listing_url, images):
        b64_images = [pybase64.urlsafe_b64encode(i).decode('utf8') for i in images]
        r = requests.post(f'http://{MAIN_NODE_IP}:8004/infer', json={
            'data_key': str(listing_url),
            'image_bytes': b64_images
        })
        inf_result = r.json()

        if inf_result.get('error'):
            logger.info(f'Error: {inf_result.get("error")}')
            return None

        self.cache.set(listing_url, inf_result)
        return inf_result
    



    def run(self, listing_url:str, listing:ExtractedData):
        cached = self.check_cache(listing_url)
        if cached:
            return cached

        logger.info('Not Cached')
      
        images = self.download_images_for_listing(listing)

        if not images:  
            logger.info('No images found')
            return {
                'boat_type': None,
                'hull_type': None,
                'style': None,
                'style_vector': None,
                'boat_type_v2': None,
                'hull_type_v2': None,
                'style_v2': None,
                'style_vector_v2': None
            }

        inf_result = self.run_inference_for_listing(listing_url, images)
        if inf_result:
            return inf_result
        logger.info('No inference result')
        return {
            'boat_type': None,
            'hull_type': None,
            'style': None,
            'style_vector': None,
            'boat_type_v2': None,
            'hull_type_v2': None,
            'style_v2': None,
            'style_vector_v2': None
        }
