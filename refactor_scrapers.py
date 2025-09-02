from interfaces.openai_client import OpenAIClient
from pydantic import BaseModel


class UrlExtractor(BaseModel):
    scraping_function: str
    extra_data_function: str | None = None
    base_url: str
    url_strings: list[str]
    page_start: int
    page_step: int


class SinglePageUrlExtractor(BaseModel):
    scraping_function: str
    extra_data_function: str | None = None
    base_url: str
    url_strings: list[str]


class InfiniteScrollUrlExtractor(BaseModel):
    scraping_function: str
    extra_data_function: str | None = None
    base_url: str
    url_strings: list[str]
    pre_scrape_function: str | None = None
    max_scrolls: int | None = None


class ButtonScrollUrlExtractor(BaseModel):
    scraping_function: str
    extra_data_function: str | None = None
    base_url: str
    url_strings: list[str]
    pre_scrape_function: str | None = None
    max_scrolls: int | None = None
    button_selector: str


class MultiPageButtonClickUrlExtractor(BaseModel):
    scraping_function: str
    extra_data_function: str | None = None
    base_url: str
    url_strings: list[str]
    pre_scrape_function: str | None = None
    button_selector: str


class DataExtractor(BaseModel):
    class_definition: str


def extract_url_extractor_multi_page_playwright(url_extractor_code):
    client = OpenAIClient()
    messages = [
        {"role": "system", "content": """
         You are a helpful assistant that extracts the url extractor code from the given code.
         you will be given the configuration for an existing url extractor written in python
         you will need to extract the following from it.
         - scraping_function: the function that is defined within the python code, this should be returned as a string and include the entire function with its definition.
         - extra_data_function: the function that may or may not be defined within the python code, this should be returned as a string and include the entire function with its definition. if no extra data function is defined, return None.
         - base_url: the base url of the website which is passed to the MultiPagePlaywrightScraper class, this should be returned as a string.
         - url_strings: the url strings that are used to scrape the website which is passed to the MultiPagePlaywrightScraper class, this should be returned as a list of strings.
         - page_start: the page number to start scraping from which is passed to the MultiPagePlaywrightScraper class, this should be returned as an integer.
         - page_step: the step to increment the page number by which is passed to the MultiPagePlaywrightScraper class, this should be returned as an integer.
         """},
        {"role": "user", "content": url_extractor_code}
    ]
    response = client.openai_stuctured_request(messages, UrlExtractor, model="gpt-4.1")
    return response




def extract_url_extractor_single_page_playwright(url_extractor_code):
    client = OpenAIClient()
    messages = [
        {"role": "system", "content": """
         You are a helpful assistant that extracts the url extractor code from the given code.
         you will be given the configuration for an existing url extractor written in python
         you will need to extract the following from it.
         - scraping_function: the function that is defined within the python code, this should be returned as a string and include the entire function with its definition.
         - extra_data_function: the function that may or may not be defined within the python code, this should be returned as a string and include the entire function with its definition. if no extra data function is defined, return None.
         - base_url: the base url of the website which is passed to the SinglePagePlaywrightScraper class, this should be returned as a string.
         - url_strings: the url strings that are used to scrape the website which is passed to the SinglePagePlaywrightScraper class, this should be returned as a list of strings.
         """},
        {"role": "user", "content": url_extractor_code}
    ]
    response = client.openai_stuctured_request(messages, SinglePageUrlExtractor, model="gpt-4.1")
    return response



def extract_url_extractor_infinite_scroll_playwright(url_extractor_code):
    client = OpenAIClient()
    messages = [
        {"role": "system", "content": """
         You are a helpful assistant that extracts the url extractor code from the given code.
         you will be given the configuration for an existing url extractor written in python
         you will need to extract the following from it.
         - scraping_function: the function that is defined within the python code, this should be returned as a string and include the entire function with its definition.
         - extra_data_function: the function that may or may not be defined within the python code, this should be returned as a string and include the entire function with its definition. if no extra data function is defined, return None.
         - base_url: the base url of the website which is passed to the InfiniteScrollPlaywrightScraper class, this should be returned as a string.
         - url_strings: the url strings that are used to scrape the website which is passed to the InfiniteScrollPlaywrightScraper class, this should be returned as a list of strings.
         - pre_scrape_function: the function that may or may not be defined within the python code, this should be returned as a string and include the entire function with its definition. if no pre scrape function is defined, return None.
         - max_scrolls: the maximum number of scrolls to perform which is passed to the InfiniteScrollPlaywrightScraper class, this should be returned as an integer.
         """},
        {"role": "user", "content": url_extractor_code}
    ]
    response = client.openai_stuctured_request(messages, InfiniteScrollUrlExtractor, model="gpt-4.1")
    return response



def extract_url_extractor_button_scroll_playwright(url_extractor_code):
    client = OpenAIClient()
    messages = [
        {"role": "system", "content": """
         You are a helpful assistant that extracts the url extractor code from the given code.
         you will be given the configuration for an existing url extractor written in python
         you will need to extract the following from it.
         - scraping_function: the function that is defined within the python code, this should be returned as a string and include the entire function with its definition.
         - extra_data_function: the function that may or may not be defined within the python code, this should be returned as a string and include the entire function with its definition. if no extra data function is defined, return None.
         - base_url: the base url of the website which is passed to the ButtonScrollPlaywrightScraper class, this should be returned as a string.
         - url_strings: the url strings that are used to scrape the website which is passed to the ButtonScrollPlaywrightScraper class, this should be returned as a list of strings.
         - pre_scrape_function: the function that may or may not be defined within the python code, this should be returned as a string and include the entire function with its definition. if no pre scrape function is defined, return None.
         - max_scrolls: the maximum number of scrolls to perform which is passed to the ButtonScrollPlaywrightScraper class, this should be returned as an integer.
         - button_selector: the selector for the button to click which is passed to the ButtonScrollPlaywrightScraper class, this should be returned as a string.
         """},
        {"role": "user", "content": url_extractor_code}
    ]
    response = client.openai_stuctured_request(messages, ButtonScrollUrlExtractor, model="gpt-4.1")
    return response


def extract_url_extractor_multi_page_button_click_playwright(url_extractor_code):
    client = OpenAIClient()
    messages = [
        {"role": "system", "content": """
         You are a helpful assistant that extracts the url extractor code from the given code.
         you will be given the configuration for an existing url extractor written in python

         you will need to extract the following from it.
         - scraping_function: the function that is defined within the python code, this should be returned as a string and include the entire function with its definition.
         - extra_data_function: the function that may or may not be defined within the python code, this should be returned as a string and include the entire function with its definition. if no extra data function is defined, return None.
         - base_url: the base url of the website which is passed to the MultiPageButtonClickPlaywrightScraper class, this should be returned as a string.
         - url_strings: the url strings that are used to scrape the website which is passed to the MultiPageButtonClickPlaywrightScraper class, this should be returned as a list of strings.
         - pre_scrape_function: the function that may or may not be defined within the python code, this should be returned as a string and include the entire function with its definition. if no pre scrape function is defined, return None.
         - button_selector: the selector for the button to click which is passed to the MultiPageButtonClickPlaywrightScraper class, this should be returned as a string.

         do not include button_selector_function in the response.
         """},
        {"role": "user", "content": url_extractor_code}
    ]
    response = client.openai_stuctured_request(messages, ButtonScrollUrlExtractor, model="gpt-4.1")
    return response




def extract_data_extractor(data_extractor_code):
    client = OpenAIClient()
    messages = [
        {"role": "system", "content": """
         You are a helpful assistant that extracts the data extractor code from the given code.
         you will be given a python script that looks like this:


```python
from applications.data_extractor.listing_scraper.new_generic_scraper import GenericScraper


class OceanIndependenceScraper(GenericScraper):
    def __init__(self):
        super().__init__('Ocean Independence', use_chatgpt=True)


    def get_features(self, soup):
        features = {}
        container = soup.find(attrs={'class':'o-section'})
        features['page_text'] = container.get_text(separator='\n', strip=True)
        return features


    def extract_description(self, soup, features, list_page_data, chatgpt_data=None):
        container = soup.find(attrs={'id':'single-yacht-overview'})
        return container.get_text(separator='\n', strip=True)
    

    def extract_image_urls(self, soup, features, list_page_data, chatgpt_data=None):
        container = soup.find(attrs={'id':'single-yacht-images'})
        a_tags = container.find_all('a', attrs={'class':'o-gallery__thumbnail'})
        urls = []
        for a_tag in a_tags:
            urls.append(a_tag['href'])
        return urls



scraper = OceanIndependenceScraper()
scraper.run()
```
         
         you will need to modify the code in the following ways:
         - remove all imports
         - replace GenericScraper with BaseScraper
         - remove the get_features method
         - remove the use_chatgpt parameter from the __init__ method
         - remove all keyword arguments from the __init__ method, there should only be the single string arg within the super call
         - remove the chatgpt_data parameter from all other methods
         - remove the class instance at the bottom of the file
         - remove the run method call at the bottom of the file

         the result should just be the class definition and the modified methods that are defined within it.
         """},
         {"role": "user", "content": data_extractor_code}
    ]
    response = client.openai_stuctured_request(messages, DataExtractor, model="gpt-4.1")
    return response


