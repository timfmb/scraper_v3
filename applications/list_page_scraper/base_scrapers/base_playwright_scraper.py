import asyncio
from random import choice
from config import PLAYWRIGHT_HEADLESS
from applications.list_page_scraper.utils.get_user_agent import get_user_agent
from interfaces.scraper_db.websites.service import get_website_by_name
from interfaces.webshare_client import WebshareClient
from bs4 import BeautifulSoup
from interfaces.scrappey_client import ScrappeyClient
import playwright
from logging_config import get_logger

logger = get_logger(__name__)


class BasePlaywrightScraper:
    def __init__(
        self,
        website_name: str
    ):
        self.website_name = website_name
        self.website = get_website_by_name(website_name)
        self.proxy_client = WebshareClient()
        self.proxy_list = self.proxy_client.list_proxies()


    async def image_route_intercept(self, route):
        try:
            if route.request.resource_type in ['image', 'media']:
                await route.abort()
            else:
                await route.continue_()
        except asyncio.CancelledError:
            return
        except Exception as e:
            return

    async def new_page(self, browser):
        try:
            if self.website.list_page_config.bypass_cloudflare:
                scrappey_client = ScrappeyClient()
                cookie_object, user_agent, proxy_obj = scrappey_client.get_config(self.website.url, self.proxy)
                context = await browser.new_context(user_agent=user_agent, proxy=proxy_obj)
                page = await context.new_page()
                await context.add_cookies(cookie_object)
                return page, context
            
            user_agent = get_user_agent()
            context = await browser.new_context(user_agent=user_agent, proxy=self.proxy)
            page = await context.new_page()
            if self.website.list_page_config.use_route_intercept:
                await page.route('**/*', self.image_route_intercept)
            return page, context 
        except Exception as e:
            await self.safe_close(browser)
            raise



    async def launch_browser(self, playwright_obj):
        self.proxy = choice(self.proxy_list) if self.website.list_page_config.use_proxy else None
        if self.website.list_page_config.browser_type == 'chromium':
            browser = await playwright_obj.chromium.launch(
                headless=PLAYWRIGHT_HEADLESS,
                proxy=self.proxy
            )
        elif self.website.list_page_config.browser_type == 'firefox':
            browser = await playwright_obj.firefox.launch(
                headless=PLAYWRIGHT_HEADLESS,
                proxy=self.proxy
            )
        elif self.website.list_page_config.browser_type == 'webkit':
            browser = await playwright_obj.webkit.launch(
                headless=PLAYWRIGHT_HEADLESS,
                proxy=self.proxy
            )
        else:
            raise ValueError('Invalid browser type')
        return browser



    async def load_page(self, page, url, retries=0):
        try:
            if not page.is_closed():  # Check if page is still open
                await page.goto(url, timeout=self.website.list_page_config.timeout)
                if self.website.list_page_config.wait_type == 'load state':
                    await page.wait_for_load_state(self.website.list_page_config.wait_for, timeout=self.website.list_page_config.timeout)
                elif self.website.list_page_config.wait_type == 'selector':
                    await page.wait_for_selector(self.website.list_page_config.wait_for, timeout=self.website.list_page_config.timeout)
                await asyncio.sleep(8)
            else:
                return None
        except Exception as e:
            if retries < 3:
                await asyncio.sleep(10)
                return await self.load_page(page, url, retries + 1)
            else:
                return None
        return page
    


    async def safe_close(self, browser, context=None, page=None):
        """Safely close all Playwright resources"""
        try:
            if page and not page.is_closed():
                await page.close()
            if context:
                await context.close()
            if browser:
                await browser.close()
        except Exception as e:
            return
        

    def _execute_string_function(self, function_string: str, soup):
        """Execute a string function with soup as parameter"""
        try:
            if not function_string:
                logger.warning(f'No function string provided: {function_string}')
                return None 
            # Create a safe execution environment with necessary imports
            # Don't include soup initially - we'll pass it as a parameter
            exec_globals = {
                'BeautifulSoup': BeautifulSoup,
                'asyncio': asyncio,
                '__builtins__': __builtins__
            }
            
            # Keep track of what was in the namespace before execution
            original_keys = set(exec_globals.keys())
            
            # Execute the function string to define it in the namespace
            exec(function_string, exec_globals)        
            # Find new callable functions that were added by the exec
            new_functions = []
            for name in exec_globals.keys():
                if (name not in original_keys and 
                    callable(exec_globals[name]) and 
                    not name.startswith('_')):
                    new_functions.append(name)
                    
            if new_functions:
                func = exec_globals[new_functions[0]]
                result = func(soup)
                return result
            else:
                    raise ValueError("No callable function found in the function string")
        except Exception as e:
            logger.error(f'Error executing string function: {e}')
            return None
        

    async def _execute_string_function_pw_page(self, function_string: str, page):
        try:
            if not function_string:
                logger.warning(f'No function string provided: {function_string}')
                return None
            exec_globals = {
                'playwright': playwright,
                'asyncio': asyncio,
                '__builtins__': __builtins__
            }

            original_keys = set(exec_globals.keys())
            exec(function_string, exec_globals)

            new_functions = []
            for name in exec_globals.keys():
                if (name not in original_keys and 
                    callable(exec_globals[name]) and 
                    not name.startswith('_')):
                    new_functions.append(name)

            if new_functions:
                func = exec_globals[new_functions[0]]
                result = await func(page)
                return result
            else:
                raise ValueError("No callable function found in the function string")
        except Exception as e:
            logger.error(f'Error executing pw page string function: {e}')
            return None
        





