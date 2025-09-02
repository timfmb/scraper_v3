from applications.uploader.uploaders.boatseekr import BoatseekrUploader
from interfaces.scraper_db.websites.service import get_all_names
import json
from applications.uploader.validation.validator import Validator
from interfaces.scraper_db.websites.service import handle_upload


    

def upload(website_name: str, validate: bool = True):
    validator = Validator(website_name)
    if validate:
        if not validator.validate():
            print(f'website {website_name} is not valid')
            return False
        print(f'website {website_name} is valid')

    uploader = BoatseekrUploader()
    uploader.run(website_name)
    handle_upload(website_name, validator.active_page_count, validator.active_page_errors)    