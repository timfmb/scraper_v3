from bs4 import BeautifulSoup
from applications.data_extractor.feature_extraction.feature_extraction import FeatureExtractor
from interfaces.scraper_db.websites.service import get_website_by_name
from interfaces.scraper_db.pages.service import set_page_extracted_data, set_page_hash, get_pages_for_website, set_page_errors
from interfaces.scraper_db.pages.models import Page, ExtractedData, InferenceResult
from hashlib import md5
import lxml
from unidecode import unidecode
from concurrent.futures import ThreadPoolExecutor
from interfaces.image_manager import ImageManager
from interfaces.inference_manager import InferenceRunner
from applications.data_extractor.model_validation.validation_manager import MODEL_VALIDATION_MANAGER
from applications.data_extractor.validation.validation import validate_listing
from applications.uploader import service as uploader_service
import markdownify as md
from logging_config import get_logger

logger = get_logger(__name__)

class BaseScraper:
    def __init__(
        self, 
        website_name
    ):
        self.website_name = website_name
        self.website = get_website_by_name(self.website_name)


    def get_section_soup(self, soup):
        return str(soup)


    def get_features(self, soup):
        feature_extractor = FeatureExtractor()
        features = feature_extractor.extract_features(soup)
        return features

    def extract_title(self, soup, features, list_page_data):
        if features.get('MAKE_DETAILS') and features.get('MODEL_DETAILS'):
            if features.get('PART_SHARE_DETAILS'):
                return features.get('MAKE_DETAILS') + ' ' + features.get('MODEL_DETAILS') + ' ' + features.get('PART_SHARE_DETAILS')
            return features.get('MAKE_DETAILS') + ' ' + features.get('MODEL_DETAILS')
        elif features.get('MAKE_DETAILS'):
            if features.get('PART_SHARE_DETAILS'):
                return features.get('MAKE_DETAILS') + ' ' + features.get('PART_SHARE_DETAILS')
            return features.get('MAKE_DETAILS')
        elif features.get('MODEL_DETAILS'):
            if features.get('PART_SHARE_DETAILS'):
                return features.get('MODEL_DETAILS') + ' ' + features.get('PART_SHARE_DETAILS')
            return features.get('MODEL_DETAILS')
        else:
            return None

    def extract_status(self, soup, features, list_page_data):
        return 'Available'

    def extract_office(self, soup, features, list_page_data):
        return None

    def extract_length(self, soup, features, list_page_data):
        return features.get('LENGTH_DETAILS')

    def extract_length_waterline(self, soup, features, list_page_data):
        return features.get('LENGTH_WATERLINE_DETAILS')

    def extract_beam(self, soup, features, list_page_data):
        return features.get('BEAM_DETAILS')

    def extract_draft(self, soup, features, list_page_data):
        return features.get('DRAFT_DETAILS')

    def extract_year(self, soup, features, list_page_data):
        return features.get('YEAR_DETAILS')

    def extract_price(self, soup, features, list_page_data):
        return features.get('PRICE_DETAILS')

    def extract_currency(self, soup, features, list_page_data):
        return features.get('CURRENCY_DETAILS')

    def extract_part_share(self, soup, features, list_page_data):
        return features.get('PART_SHARE_DETAILS')

    def extract_vat_status(self, soup, features, list_page_data):
        return features.get('VAT_STATUS_DETAILS')

    def extract_location(self, soup, features, list_page_data):
        return features.get('LOCATION_DETAILS')

    def extract_country(self, soup, features, list_page_data):
        return features.get('COUNTRY_DETAILS')

    def extract_make(self, soup, features, list_page_data):
        return features.get('MAKE_DETAILS')

    def extract_model(self, soup, features, list_page_data):
        return features.get('MODEL_DETAILS')

    def extract_make_model(self, soup, features, list_page_data):
        return features.get('MAKE_DETAILS') + ' ' + features.get('MODEL_DETAILS')

    def extract_condition(self, soup, features, list_page_data):
        return features.get('CONDITION_DETAILS')

    def extract_boat_type(self, soup, features, list_page_data):
        return features.get('BOAT_TYPE_DETAILS')

    def extract_category(self, soup, features, list_page_data):
        return features.get('CATEGORY_DETAILS')

    def extract_construction(self, soup, features, list_page_data):
        return features.get('CONSTRUCTION_DETAILS')

    def extract_keel_type(self, soup, features, list_page_data):
        return features.get('KEEL_TYPE_DETAILS')

    def extract_ballast(self, soup, features, list_page_data):
        return features.get('BALLAST_DETAILS')

    def extract_displacement(self, soup, features, list_page_data):
        return features.get('DISPLACEMENT_DETAILS')

    def extract_designer(self, soup, features, list_page_data):
        return features.get('DESIGNER_DETAILS')

    def extract_builder(self, soup, features, list_page_data):
        return features.get('BUILDER_DETAILS')

    def extract_cabins(self, soup, features, list_page_data):
        return features.get('CABINS_DETAILS')

    def extract_berths(self, soup, features, list_page_data):
        return features.get('BERTHS_DETAILS')

    def extract_heads(self, soup, features, list_page_data):
        return features.get('HEADS_DETAILS')

    def extract_boat_name(self, soup, features, list_page_data):
        return None

    def extract_range(self, soup, features, list_page_data):
        return features.get('RANGE_DETAILS')

    def extract_passenger_capacity(self, soup, features, list_page_data):
        return features.get('PASSENGER_CAPACITY_DETAILS')

    def extract_engine_count(self, soup, features, list_page_data):
        return features.get('ENGINE_COUNT_DETAILS')

    def extract_fuel_type(self, soup, features, list_page_data):
        return features.get('FUEL_TYPE_DETAILS')

    def extract_fuel_tankage(self, soup, features, list_page_data):
        return features.get('FUEL_TANK_SIZE_DETAILS')

    def extract_engine_hours(self, soup, features, list_page_data):
        return features.get('ENGINE_HOURS_DETAILS')

    def extract_engine_power(self, soup, features, list_page_data):
        return features.get('ENGINE_POWER_DETAILS')

    def extract_engine_manufacturer(self, soup, features, list_page_data):
        return features.get('ENGINE_MANUFACTURER_DETAILS')

    def extract_engine_model(self, soup, features, list_page_data):
        return features.get('ENGINE_MODEL_DETAILS')

    def extract_engine_location(self, soup, features, list_page_data):
        return features.get('ENGINE_LOCATION_DETAILS')

    def extract_engine_drive_type(self, soup, features, list_page_data):
        return features.get('ENGINE_DRIVE_TYPE_DETAILS')

    def extract_maximum_speed(self, soup, features, list_page_data):
        return features.get('MAXIMUM_SPEED_DETAILS')

    def extract_cruising_speed(self, soup, features, list_page_data):
        return features.get('CRUISING_SPEED_DETAILS')

    def extract_prop_type(self, soup, features, list_page_data):
        return features.get('PROP_TYPE_DETAILS')

    def extract_description(self, soup, features, list_page_data):
        return None

    def extract_image_urls(self, soup, features, list_page_data):
        return None
    

    def extract_attribute(self, feature_name, func, soup, features, list_page_data, out_type):
        try:
            result = func(soup, features, list_page_data)
            if result is None:
                if feature_name in ['country', 'currency', 'location']:
                    return self.website.detail_page_config.defaults.model_dump().get(feature_name)
                return None
            return out_type(result)
        except Exception as e:
            return None
        

    def _clean_text_data(self, data_dict):
        """Clean text data using unidecode."""
        cleaned_dict = {}
        for key, value in data_dict.items():
            try:
                if isinstance(key, str) and isinstance(value, str):
                    key = unidecode(key)
                    value = unidecode(value)
                cleaned_dict[key] = value
            except Exception:
                cleaned_dict[key] = value
        return cleaned_dict
    

    def clean_image_urls(self, image_urls):
        try:
            if not image_urls:
                return []
            
            cleaned_image_urls = []
            for url in image_urls:
                if url == None:
                    continue
                if url not in cleaned_image_urls and 'youtube.com' not in url and 'youtu.be' not in url and '.mp4' not in url and url.startswith('http'):
                    cleaned_image_urls.append(url)
            return cleaned_image_urls
        except Exception as e:
            return []
        

    def _process_images(self, data):
        """Process and download images."""
        image_manager = ImageManager()
        if data['image_urls']:
            data['image_download_urls'] = image_manager.download_images(data['image_urls'])
        else:
            data['image_download_urls'] = []
        return data
        


    def _extract_all_attributes(self, soup, features, list_page_data, url):
        """Extract all attributes using the extract_ methods."""
        return {
            'title': self.extract_attribute('title', self.extract_title, soup, features, list_page_data, str),
            'status': self.extract_attribute('status', self.extract_status, soup, features, list_page_data, str),
            'office': self.extract_attribute('office', self.extract_office, soup, features, list_page_data, int),
            'length': self.extract_attribute('length', self.extract_length, soup, features, list_page_data, float),
            'length_waterline': self.extract_attribute('length_waterline', self.extract_length_waterline, soup, features, list_page_data, float),
            'beam': self.extract_attribute('beam', self.extract_beam, soup, features, list_page_data, float),
            'draft': self.extract_attribute('draft', self.extract_draft, soup, features, list_page_data, float),
            'year': self.extract_attribute('year', self.extract_year, soup, features, list_page_data, int),
            'price': self.extract_attribute('price', self.extract_price, soup, features, list_page_data, int),
            'currency': self.extract_attribute('currency', self.extract_currency, soup, features, list_page_data, str),
            'part_share': self.extract_attribute('part_share', self.extract_part_share, soup, features, list_page_data, str),
            'vat_status': self.extract_attribute('vat_status', self.extract_vat_status, soup, features, list_page_data, bool),
            'location': self.extract_attribute('location', self.extract_location, soup, features, list_page_data, str),
            'country': self.extract_attribute('country', self.extract_country, soup, features, list_page_data, str),
            'make': self.extract_attribute('make', self.extract_make, soup, features, list_page_data, str),
            'model': self.extract_attribute('model', self.extract_model, soup, features, list_page_data, str),
            'make_model': self.extract_attribute('make_model', self.extract_make_model, soup, features, list_page_data, str),
            'condition': self.extract_attribute('condition', self.extract_condition, soup, features, list_page_data, str),
            'construction': self.extract_attribute('construction', self.extract_construction, soup, features, list_page_data, str),
            'keel_type': self.extract_attribute('keel_type', self.extract_keel_type, soup, features, list_page_data, str),
            'ballast': self.extract_attribute('ballast', self.extract_ballast, soup, features, list_page_data, int),
            'displacement': self.extract_attribute('displacement', self.extract_displacement, soup, features, list_page_data, int),
            'designer': self.extract_attribute('designer', self.extract_designer, soup, features, list_page_data, str),
            'builder': self.extract_attribute('builder', self.extract_builder, soup, features, list_page_data, str),
            'cabins': self.extract_attribute('cabins', self.extract_cabins, soup, features, list_page_data, int),
            'berths': self.extract_attribute('berths', self.extract_berths, soup, features, list_page_data, int),
            'heads': self.extract_attribute('heads', self.extract_heads, soup, features, list_page_data, int),
            'boat_name': self.extract_attribute('boat_name', self.extract_boat_name, soup, features, list_page_data, str),
            'range': self.extract_attribute('range', self.extract_range, soup, features, list_page_data, int),
            'passenger_capacity': self.extract_attribute('passenger_capacity', self.extract_passenger_capacity, soup, features, list_page_data, int),
            'engine_count': self.extract_attribute('engine_count', self.extract_engine_count, soup, features, list_page_data, int),
            'fuel_type': self.extract_attribute('fuel_type', self.extract_fuel_type, soup, features, list_page_data, str),
            'fuel_tankage': self.extract_attribute('fuel_tankage', self.extract_fuel_tankage, soup, features, list_page_data, int),
            'engine_hours': self.extract_attribute('engine_hours', self.extract_engine_hours, soup, features, list_page_data, int),
            'engine_power': self.extract_attribute('engine_power', self.extract_engine_power, soup, features, list_page_data, int),
            'engine_manufacturer': self.extract_attribute('engine_manufacturer', self.extract_engine_manufacturer, soup, features, list_page_data, str),
            'engine_model': self.extract_attribute('engine_model', self.extract_engine_model, soup, features, list_page_data, str),
            'engine_location': self.extract_attribute('engine_location', self.extract_engine_location, soup, features, list_page_data, str),
            'engine_drive_type': self.extract_attribute('engine_drive_type', self.extract_engine_drive_type, soup, features, list_page_data, str),
            'maximum_speed': self.extract_attribute('maximum_speed', self.extract_maximum_speed, soup, features, list_page_data, int),
            'cruising_speed': self.extract_attribute('cruising_speed', self.extract_cruising_speed, soup, features, list_page_data, int),
            'prop_type': self.extract_attribute('prop_type', self.extract_prop_type, soup, features, list_page_data, str),
            'description': self.extract_attribute('description', self.extract_description, soup, features, list_page_data, str),
            'image_urls': self.clean_image_urls(self.extract_attribute('image_urls', self.extract_image_urls, soup, features, list_page_data, list)),
            'url': url,
            'features': features,
            'list_page_data': list_page_data
        }
    

    def _page_changed(self, page: Page, section_html: str):
        current_hash = md5(md.markdownify(section_html).encode()).hexdigest()
        if not page.hash or not page.extracted_data:
            return True
        
        if current_hash == page.hash:
            logger.debug(f"Page {page.url} has not changed")
            return False
        
        return True
    

    def pull_forward_data(self, page: Page, extracted_data: dict):
        if not page.extracted_data:
            return extracted_data
        
        previous_data = page.extracted_data.model_dump()
        if page.extracted_data:
            for key, value in extracted_data.items():
                if value is None and previous_data.get(key) is not None:
                    extracted_data[key] = previous_data[key]
        return extracted_data

            


    def scrape_page(self, page: Page, full_scrape=False):
        """Main method to scrape a URL and extract listing data."""
        if not page.html:
            return

        soup = BeautifulSoup(page.html, 'lxml')

        section_soup = self.get_section_soup(soup)

        page_changed = self._page_changed(page, section_soup)
        
        if page_changed or full_scrape:
            logger.info(f"Extracting data for {page.url}")
            features = self.get_features(section_soup)
            if page.list_page_data:
                page.list_page_data = self._clean_text_data(page.list_page_data)

            extracted_data = self._extract_all_attributes(soup, features, page.list_page_data, page.url)
            extracted_data = self.pull_forward_data(page, extracted_data)
            set_page_hash(page.url, md5(md.markdownify(section_soup).encode()).hexdigest())
        
        else:
            extracted_data = page.extracted_data.model_dump()

        extracted_data = self._process_images(extracted_data)

        extracted_data = ExtractedData(**extracted_data)
        inference_manager = InferenceRunner()
        inference_result = inference_manager.run(page.url, extracted_data)
        extracted_data.inference_result = InferenceResult(**inference_result)
        
        if extracted_data.inference_result.style_vector_v2:
            validation_result = MODEL_VALIDATION_MANAGER.validate(
                page.url,
                extracted_data.inference_result.style_vector_v2,
                extracted_data.make,
                extracted_data.model
            )
        else:
            validation_result = {
                'valid': False,
                'make': None,
                'model': None
            }
        extracted_data = extracted_data.model_dump()
        if validation_result.get('valid') == True:
            extracted_data['validated_make'] = validation_result.get('make')
            extracted_data['validated_model'] = validation_result.get('model')
        else:
            extracted_data['validated_make'] = None
            extracted_data['validated_model'] = None


        errors = validate_listing(extracted_data)

        extracted_data = ExtractedData(**extracted_data)


        set_page_extracted_data(page.url, extracted_data.model_dump())
        set_page_errors(page.url, errors)

        



    def run(self, full_scrape=False):
        if self.website is None:
            raise ValueError(f"Website {self.website_name} not found")
        
        pages = get_pages_for_website(self.website_name, active=True)
        
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(self.scrape_page, page, full_scrape) for page in pages]
            for future in futures:
                future.result()
        
        uploader_service.upload(self.website_name)
