class Scraper(BaseScraper):
    def __init__(self):
        super().__init__('McMichael Yacht Brokers')

    def extract_description(self, soup, features, list_page_data):
        # Step 1: Try to find the description container (e.g., a div with id 'description')
        desc_container = soup.find('div', {'class': 'intro-container'})
        return desc_container.get_text(separator=' ', strip=True) if desc_container else ''

    def extract_image_urls(self, soup, features, list_page_data):
        container = soup.find('div', class_='gridzy-v1Container')
        urls = []
        a_tags = container.find_all('a')
        for a_tag in a_tags:
            urls.append(a_tag['href'])
        return urls
