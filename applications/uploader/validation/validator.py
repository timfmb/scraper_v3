from interfaces.scraper_db.websites.service import get_website_by_name
from interfaces.scraper_db.pages.service import count_pages_for_website, get_active_page_error_counts_for_website


class Validator:
    def __init__(self, website_name: str):
        self.website_name = website_name
        self.website = get_website_by_name(website_name)
        self.active_page_errors = get_active_page_error_counts_for_website(website_name)
        self.active_page_count = count_pages_for_website(website_name, active=True)


    def validate_page_count(self):
        if self.active_page_count < self.website.last_listing_count * 0.9:
            return False
        return True
    

    def validate_error_counts(self):
        valid = True
        for error, count in self.active_page_errors.items():
            if error not in self.website.last_error_counts:
                valid = False
            if self.website.last_error_counts[error] < count:
                valid = False
        return valid
    
    def validate(self):
        print(f'validating {self.website_name}')
        if not self.validate_page_count():
            print('page count is not valid')
            return False
        if not self.validate_error_counts():
            print('error counts are not valid')
            return False
        print('validation successful')
        return True