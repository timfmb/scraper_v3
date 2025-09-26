from ..client import get_db
from .models import Website, ListPageConfig, DetailPageConfig
from .service import get_website_by_name
from logging_config import get_logger

logger = get_logger(__name__)




def get_collection():
    db = get_db()
    return db['websites']


class ScraperBuilder:
    def __init__(self):
        self.website = None

    def create_website(
        self,
        url: str, 
        name:str,
        tags: list[str] = []
    ):
        website = get_website_by_name(name)
        if website:
            logger.warning(f'Website {name} already exists')
            raise ValueError(f'Website {name} already exists')
        website = Website(url=url, name=name, tags=tags)
        self.website = website


    def create_single_page_playwright_config(
        self,
        wait_type: str = 'load state',
        wait_for: str = 'domcontentloaded',
        use_route_intercept: bool = True,
        browser_type: str = 'chromium',
        use_proxy: bool = True,
        timeout: int = 90000,
        url_strings: list[str] = [],
        scraping_function: str = None, 
        extra_data_function: str = None
    ):
        config = ListPageConfig(
            wait_type=wait_type,
            wait_for=wait_for,
            use_route_intercept=use_route_intercept,
            browser_type=browser_type,
            use_proxy=use_proxy,
            timeout=timeout,
            url_strings=url_strings,
            scraping_function=scraping_function,
            extra_data_function=extra_data_function
        )
        self.website.list_page_config = config
        self.website.list_page_scraper_type = 'single_page_playwright'



    def create_multi_page_playwright_config(
        self,
        wait_type: str = 'load state',
        wait_for: str = 'domcontentloaded',
        use_route_intercept: bool = True,
        browser_type: str = 'chromium',
        use_proxy: bool = True,
        timeout: int = 90000,
        url_strings: list[str] = [],
        scraping_function: str | None = None,
        extra_data_function: str | None = None,
        page_start: int = 1,
        page_step: int = 1,
        max_pages: int | None = None,
        max_retries: int = 5
    ):
        config = ListPageConfig(
            wait_type=wait_type,
            wait_for=wait_for,
            use_route_intercept=use_route_intercept,
            browser_type=browser_type,
            use_proxy=use_proxy,
            timeout=timeout,
            url_strings=url_strings,
            scraping_function=scraping_function,
            extra_data_function=extra_data_function,
            page_start=page_start,
            page_step=page_step,
            max_pages=max_pages,
            max_retries=max_retries
        )
        self.website.list_page_config = config
        self.website.list_page_scraper_type = 'multi_page_playwright'

    def create_infinite_scroll_playwright_config(
        self,
        wait_type: str = 'load state',
        wait_for: str = 'domcontentloaded',
        use_route_intercept: bool = True,
        browser_type: str = 'chromium',
        use_proxy: bool = True,
        timeout: int = 90000,
        url_strings: list[str] = [],
        scraping_function: str | None = None,
        extra_data_function: str | None = None,
        pre_scrape_function: str | None = None,
        max_scrolls: int | None = None,
    ):
        config = ListPageConfig(
            wait_type=wait_type,
            wait_for=wait_for,
            use_route_intercept=use_route_intercept,
            browser_type=browser_type,
            use_proxy=use_proxy,
            timeout=timeout,
            url_strings=url_strings,
            scraping_function=scraping_function,
            extra_data_function=extra_data_function,
            pre_scrape_function=pre_scrape_function,
            max_scrolls=max_scrolls
        )
        self.website.list_page_config = config
        self.website.list_page_scraper_type = 'infinite_scroll_playwright'

    def create_button_scroll_playwright_config(
        self,
        wait_type: str = 'load state',
        wait_for: str = 'domcontentloaded',
        use_route_intercept: bool = True,
        browser_type: str = 'chromium',
        use_proxy: bool = True,
        timeout: int = 90000,
        url_strings: list[str] = [],
        scraping_function: str | None = None,
        extra_data_function: str | None = None,
        pre_scrape_function: str | None = None,
        max_scrolls: int | None = None,
        button_selector: str = None,
    ):
        config = ListPageConfig(
            wait_type=wait_type,
            wait_for=wait_for,
            use_route_intercept=use_route_intercept,
            browser_type=browser_type,
            use_proxy=use_proxy,
            timeout=timeout,
            url_strings=url_strings,
            scraping_function=scraping_function,
            extra_data_function=extra_data_function,
            pre_scrape_function=pre_scrape_function,
            max_scrolls=max_scrolls,
            button_selector=button_selector
        )
        self.website.list_page_config = config
        self.website.list_page_scraper_type = 'button_scroll_playwright'

    def create_multi_page_button_click_playwright_config(
        self,
        wait_type: str = 'load state',
        wait_for: str = 'domcontentloaded',
        use_route_intercept: bool = True,
        browser_type: str = 'chromium',
        use_proxy: bool = True,
        timeout: int = 90000,
        url_strings: list[str] = [],
        scraping_function: str | None = None,
        extra_data_function: str | None = None,
        pre_scrape_function: str | None = None,
        button_selector: str = None,
    ):
        config = ListPageConfig(
            wait_type=wait_type,
            wait_for=wait_for,
            use_route_intercept=use_route_intercept,
            browser_type=browser_type,
            use_proxy=use_proxy,
            timeout=timeout,
            url_strings=url_strings,
            scraping_function=scraping_function,
            extra_data_function=extra_data_function,
            pre_scrape_function=pre_scrape_function,
            button_selector=button_selector
        )
        self.website.list_page_config = config
        self.website.list_page_scraper_type = 'multi_page_button_click_playwright'


    def create_detail_page_config(
        self,
        scraper_string: str
    ):
        config = DetailPageConfig(scraper_string=scraper_string)
        self.website.detail_page_config = config


    def save(self):
        collection = get_collection()
        collection.insert_one(self.website.model_dump())
