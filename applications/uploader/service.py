from applications.uploader.uploaders.boatseekr import BoatseekrUploader
from interfaces.scraper_db.websites.service import get_all_names, mark_as_invalid, mark_as_valid
import json
from applications.uploader.validation.validator import Validator
from interfaces.scraper_db.websites.service import handle_upload
from logging_config import get_logger

logger = get_logger(__name__)


def upload(website_name: str, validate: bool = True):
    validator = Validator(website_name)
    if validate:
        if not validator.validate():
            logger.warning(f'website {website_name} is not valid')
            mark_as_invalid(website_name)
            return False
        logger.info(f'website {website_name} is valid')

    uploader = BoatseekrUploader()
    uploader.run(website_name)
    handle_upload(website_name, validator.active_page_count, validator.active_page_errors)    