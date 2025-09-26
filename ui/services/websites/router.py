from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import interfaces.scraper_db.websites.service as websites_service
import interfaces.scraper_db.pages.service as pages_service
from pydantic import BaseModel
from typing import Literal
from applications.uploader.service import upload
from interfaces.scraper_db.websites.service import handle_upload

router = APIRouter(
    prefix='/websites',
    tags=['websites']
)


@router.get('/')
def get_websites():
    with open('ui/services/websites/templates/websites.html', 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())
    

@router.get('/website/{website_name}')
def get_website(website_name: str):
    with open('ui/services/websites/templates/website.html', 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())
    

@router.get('/website/{website_name}/data')
def get_website_data(website_name: str):
    website = websites_service.get_website_by_name(website_name)
    website = website.model_dump()
    website['pages'] = [page.model_dump() for page in pages_service.get_pages_for_website(website_name, active=True)]
    return website
    

@router.get('/all')
def get_websites():
    websites = websites_service.get_all_websites()
    built_websites = []
    for website in websites:
        website = website.model_dump()
        
        # Current data
        current_pages = pages_service.count_pages_for_website(website['name'], active=True)
        errors = pages_service.get_active_page_errors_for_website(website['name'])
        current_error_counts = {}
        for page_errors in errors:
            for error in page_errors:
                if error in current_error_counts:
                    current_error_counts[error] += 1
                else:
                    current_error_counts[error] = 1
        current_error_counts = dict(sorted(current_error_counts.items(), key=lambda item: item[0]))
        
        # Structure data with current and previous values
        website['pages'] = current_pages
        website['errors'] = current_error_counts
        website['previous_pages'] = website.get('last_listing_count', 0) or 0
        website['previous_errors'] = website.get('last_error_counts', {}) or {}
        
        built_websites.append(website)
    return built_websites

    
@router.get('/tag/{tag}')
def websites_by_tag(tag: str):
    websites = websites_service.get_website_by_tag(tag)
    for website in websites:
        website = website.model_dump()
        website['pages'] = pages_service.count_pages_for_website(website['name'])
    return websites


@router.get('/tags')
def all_tags():
    return websites_service.get_all_tags()


@router.get('/error-types')
def get_all_error_types():
    """Get all unique error types across all websites"""
    websites = websites_service.get_all_websites()
    all_error_types = set()
    
    for website in websites:
        errors = pages_service.get_active_page_errors_for_website(website.name)
        for page_errors in errors:
            for error in page_errors:
                all_error_types.add(error)
    
    return sorted(list(all_error_types))


class UpdateListPageScrapingFunctionRequest(BaseModel):
    website_name: str
    function: str


@router.post('/update-list-page-scraping-function')
def update_list_page_scraping_function(request: UpdateListPageScrapingFunctionRequest):
    websites_service.update_list_page_scraping_function(request.website_name, request.function)
    return {'message': 'List page scraping function updated successfully'}


class UpdateListPageExtraDataFunctionRequest(BaseModel):
    website_name: str
    function: str

@router.post('/update-list-page-extra-data-function')
def update_list_page_extra_data_function(request: UpdateListPageExtraDataFunctionRequest):
    websites_service.update_list_page_extra_data_function(request.website_name, request.function)
    return {'message': 'List page extra data function updated successfully'}


class UpdateListPagePreScrapeFunctionRequest(BaseModel):
    website_name: str
    function: str

@router.post('/update-list-page-pre-scrape-function')
def update_list_page_pre_scrape_function(request: UpdateListPagePreScrapeFunctionRequest):
    websites_service.update_list_page_pre_scrape_function(request.website_name, request.function)
    return {'message': 'List page pre scrape function updated successfully'}

class UpdateDetailPageScraperStringRequest(BaseModel):
    website_name: str
    scraper_string: str

@router.post('/update-detail-page-scraper-string')
def update_detail_page_scraper_string(request: UpdateDetailPageScraperStringRequest):
    websites_service.update_detail_page_scraper_string(request.website_name, request.scraper_string)
    return {'message': 'Detail page scraper string updated successfully'}


class UpdateListPageConfigSettingsRequest(BaseModel):
    website_name: str
    wait_type: Literal['load state']
    wait_for: Literal['domcontentloaded', 'networkidle']
    use_route_intercept: bool
    browser_type: Literal['chromium', 'firefox']
    use_proxy: bool
    bypass_cloudflare: bool
    url_strings: list[str]
    timeout: int = 90000
    page_start: int|None = None
    page_step: int|None = None
    max_retries: int|None = None
    max_pages: int|None = None

@router.post('/update-list-page-config-settings')
def update_list_page_config_settings(request: UpdateListPageConfigSettingsRequest):
    websites_service.update_list_page_config_settings(
        request.website_name,
        request.wait_type,
        request.wait_for,
        request.use_route_intercept,
        request.browser_type,
        request.use_proxy,
        request.bypass_cloudflare,
        request.url_strings,
        request.timeout,
        request.page_start,
        request.page_step,
        request.max_retries,
        request.max_pages
    )


class UpdateDetailPageConfigSettingsRequest(BaseModel):
    website_name: str
    wait_until: Literal['load', 'domcontentloaded', 'networkidle']
    wait_for_selector: str|None = None


@router.post('/update-detail-page-config-settings')
def update_detail_page_config_settings(request: UpdateDetailPageConfigSettingsRequest):
    websites_service.update_detail_page_config_settings(
        request.website_name,
        request.wait_until,
        request.wait_for_selector
    )
    return {'message': 'Detail page config settings updated successfully'}


class UpdateDefaultsRequest(BaseModel):
    website_name: str
    location: str|None = None
    country: str|None = None
    currency: str|None = None

@router.post('/update-defaults')
def update_defaults(request: UpdateDefaultsRequest):
    websites_service.update_defaults(request.website_name, request.location, request.country, request.currency)
    return {'message': 'Defaults updated successfully'}


class DeleteAllHtmlForWebsiteRequest(BaseModel):
    website_name: str

@router.post('/delete-all-html-for-website')
def delete_all_html_for_website(request: DeleteAllHtmlForWebsiteRequest):
    pages_service.delete_all_html_for_website(request.website_name)
    return {'message': 'All HTML for website deleted successfully'}


class UploadWebsiteRequest(BaseModel):
    website_name: str
    new_listing_count: int
    new_error_counts: dict


@router.post('/upload')
def upload_website(request: UploadWebsiteRequest):
    upload(request.website_name, validate=False)
    return {'message': 'Uploaded successfully'}
    
