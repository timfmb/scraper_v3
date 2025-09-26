from applications.uploader.data_models import BoatListing
from applications.uploader.cleaning.description import clean_description
from applications.uploader.cleaning.country import clean_country
from applications.uploader.cleaning.images import clean_images
from interfaces.currency_converter import CurrencyConverter
from interfaces.scraper_db.pages.service import get_pages_for_website
from interfaces.scraper_db.pages.models import Page
from interfaces.vec_utils import normalize_to_int8, generate_bson_vector
from applications.uploader.location.locations import Locationvalidator
from concurrent.futures import ThreadPoolExecutor
from interfaces.atlas_db import get_atlas_search_engine_db
from hashlib import md5
from datetime import datetime
import json
from time import time
from logging_config import get_logger

logger = get_logger(__name__)



class ListingBuilder:
    def __init__(self, raw_listing: dict, url:str, website_name:str):
        self.raw_listing = raw_listing
        self.url = url
        self.website_name = website_name


    def clean_listing(self):
        if self.raw_listing.get('description'):
            self.raw_listing['description'] = clean_description(self.raw_listing['description'], self.url)

        if self.raw_listing.get('country'):
            self.raw_listing['country'] = clean_country(self.raw_listing['country'])

        if self.raw_listing.get('image_download_urls'):
            self.raw_listing['image_download_urls'] = clean_images(self.raw_listing['image_download_urls'])

    def restructure_inferred_data(self):
        if self.raw_listing.get('inference_result'):
            self.raw_listing['boat_type_v2'] = self.raw_listing['inference_result'].get('boat_type_v2')
            self.raw_listing['hull_type_v2'] = self.raw_listing['inference_result'].get('hull_type_v2')
            self.raw_listing['style_v2'] = self.raw_listing['inference_result'].get('style_v2')
            self.raw_listing['style_vector_v2'] = self.raw_listing['inference_result'].get('style_vector_v2')
        del self.raw_listing['inference_result']

    def add_website_name_and_url(self):
        self.raw_listing['broker'] = self.website_name
        self.raw_listing['url'] = self.url


    def restructure_images(self):
        images = []
        if self.raw_listing.get('image_download_urls'):
            for image_url in self.raw_listing['image_download_urls']:
                images.append(image_url)
            del self.raw_listing['image_download_urls']
            del self.raw_listing['image_urls']
        self.raw_listing['image_url'] = images[0]
        self.raw_listing['images'] = images


    def convert_price_to_usd(self):
        if self.raw_listing.get('price') and self.raw_listing.get('currency'):
            currency_converter = CurrencyConverter()
            self.raw_listing['price_usd'] = int(currency_converter.convert_to_usd(self.raw_listing['price'], self.raw_listing['currency']))
        else:
            self.raw_listing['price_usd'] = None


    def validate_location(self):
        if self.raw_listing.get('country') in ['New Zealand', 'Australia', 'United States']:
            location_validator = Locationvalidator()
            inferred_location, country = location_validator.validate_location(self.raw_listing['location'], self.raw_listing['country'])
            if inferred_location:
                self.raw_listing['search_location'] = inferred_location
                logger.info(f'validated location {inferred_location} for {self.raw_listing["url"]}')
            else:
                self.raw_listing['search_location'] = None
                logger.info(f'could not validate location for {self.raw_listing["location"]} in {self.raw_listing["country"]}')
        else:
            self.raw_listing['search_location'] = None


    def build_vector(self, listing: dict):
        try:
            vector = normalize_to_int8(listing['style_vector_v2'])
            vector = generate_bson_vector(vector)
            listing['style_vector_int8'] = vector
        except Exception as e:
            logger.info(f'error in build_vector: {e}')
            listing['style_vector_int8'] = None
        
        return listing


    def build_listing(self) -> dict:
        self.clean_listing()
        self.restructure_inferred_data()
        self.add_website_name_and_url()
        self.restructure_images()
        self.convert_price_to_usd()
        self.validate_location()
        listing = BoatListing(**self.raw_listing).model_dump()
        listing = self.build_vector(listing)
        logger.info(listing['search_location'])
        return listing



class Uploader:
    def __init__(self):
        self.db = get_atlas_search_engine_db()


    def build_hash(self, listing: dict):
        data_to_hash = {
            'title': listing['title'],
            'price': listing['price'],
            'currency': listing['currency'],
            'country': listing['country'],
            'location': listing['location'],
            'search_location': listing['search_location'],
            'make': listing['make'],
            'model': listing['model'],
            'make_model': listing['make_model'],
            'condition': listing['condition'],
            'construction': listing['construction'],
            'keel_type': listing['keel_type'],
            'ballast': listing['ballast'],
            'displacement': listing['displacement'],
            'designer': listing['designer'],
            'builder': listing['builder'],
            'cabins': listing['cabins'],
            'berths': listing['berths'],
            'heads': listing['heads'],
            'boat_name': listing['boat_name'],
            'range': listing['range'],
            'passenger_capacity': listing['passenger_capacity'],
            'engine_count': listing['engine_count'],
            'fuel_type': listing['fuel_type'],
            'fuel_tankage': listing['fuel_tankage'],
            'engine_hours': listing['engine_hours'],
            'engine_power': listing['engine_power'],
            'engine_manufacturer': listing['engine_manufacturer'],
            'engine_model': listing['engine_model'],
            'engine_location': listing['engine_location'],
            'engine_drive_type': listing['engine_drive_type'],
            'maximum_speed': listing['maximum_speed'],
            'cruising_speed': listing['cruising_speed'],
            'prop_type': listing['prop_type'],
            'description': listing['description'],
            'image_url': listing['image_url'],
            'images': listing['images'],
        }
        return md5(json.dumps(data_to_hash).encode()).hexdigest()


    def check_if_listing_exists(self, listing: dict):
        current = self.db['Boatseekr'].find_one({'url': listing['url']}, {'url': 1, "hash": 1})
        if current:
            return True, current.get('hash')
        else:
            return False, None
        

    def hash_changed(self, listing: dict, current_hash: str):
        new_hash = self.build_hash(listing)
        if new_hash == current_hash:
            return False, None
        else:
            return True, new_hash



    def update_listing(self, listing: dict, new_hash: str):
        logger.info(f'updating listing {listing["url"]}')
        listing['last_scraped'] = datetime.now()
        listing['active'] = True
        listing['hash'] = new_hash
        self.db['Boatseekr'].update_one({'url': listing['url']}, {'$set': listing})
        logger.info(f'updated listing {listing["url"]}')
        return listing
    

    def create_listing(self, listing: dict, new_hash: str):
        logger.info(f'creating listing {listing["url"]}')
        listing['date_added'] = datetime.now().strftime('%d-%m-%Y')
        listing['last_scraped'] = datetime.now()
        listing['active'] = True
        listing['hash'] = new_hash
        self.db['Boatseekr'].insert_one(listing)
        logger.info(f'created listing {listing["url"]}')
        return listing
        

    def run(self, listing: dict):
        try:
            exists, current_hash = self.check_if_listing_exists(listing)
            if exists:
                changed, new_hash = self.hash_changed(listing, current_hash)
                if changed:
                    self.update_listing(listing, new_hash)
                else:
                    logger.info(f'listing {listing["url"]} has not changed')
            else:
                new_hash = self.build_hash(listing)
                self.create_listing(listing, new_hash)
        except Exception as e:
            logger.info(f'error in run: {e}')
            return None


    def deactivate_old_listings(self, urls_to_keep: list[str], website_name: str):
        deactivated = self.db['Boatseekr'].update_many({'broker':website_name, 'url': {'$nin': urls_to_keep}, 'active': True}, {'$set': {'active': False}})
        if deactivated.modified_count > 0:
            logger.info(f'deactivated {deactivated.modified_count} listings')
            return True
        else:
            logger.info(f'no listings to deactivate')
            return False
    

        
    



class BoatseekrUploader:
    def __init__(self):
        self.uploader = Uploader()


    def build_page(self, page: Page):
        try:
            page = page.model_dump()
            builder = ListingBuilder(page['extracted_data'], page['url'], page['website_name'])
            listing = builder.build_listing()
            return listing
        except Exception as e:
            logger.info(f'error in build_page: {e}')
            return None

    def run(self, website_name: str):
        pages = get_pages_for_website(website_name, active=True)
        with ThreadPoolExecutor(max_workers=10) as executor:
            listings = executor.map(self.build_page, pages)
        
        listings = [listing for listing in listings if listing is not None]
        logger.info(f'built {len(listings)} listings')
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.uploader.run, listings)
        logger.info(f'ran {len(listings)} listings')
        urls_to_keep = [listing['url'] for listing in listings]
        self.uploader.deactivate_old_listings(urls_to_keep, website_name)

