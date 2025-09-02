from pydantic import BaseModel
from datetime import datetime
from typing import Callable



class ListPageConfig(BaseModel):
    wait_type: str = 'load state'
    wait_for: str = 'domcontentloaded'
    use_route_intercept: bool = True
    pre_scrape_function: str | None = None
    max_scrolls: int | None = None
    browser_type: str = 'chromium'
    use_proxy: bool = True
    bypass_cloudflare: bool = False
    timeout: int = 90000
    url_strings: list[str] = []
    scraping_function: str | None = None
    extra_data_function: str | None = None
    button_selector: str | None = None
    page_start: int = 1
    page_step: int = 1
    max_pages: int | None = None
    max_retries: int = 5


class Defaults(BaseModel):
    location: str | None = None
    country: str | None = None
    currency: str | None = None


class DetailPageConfig(BaseModel):
    scraper_string: str | None = None
    wait_until: str | None = None
    wait_for_selector: str | None = None
    defaults: Defaults = None


class Website(BaseModel):
    url: str
    name: str
    tags: list[str] = []
    list_page_scraper_type:str | None = None
    page_scraper_time_delta: int = 86400 * 2
    list_page_config: ListPageConfig | None = None
    detail_page_config: DetailPageConfig | None = None
    last_listing_count: int | None = None
    last_error_counts: dict = {}
    last_scrape_valid: bool = False
    last_upload_date: datetime | None = None