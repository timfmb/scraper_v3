class Scraper(BaseScraper):
    def __init__(self):
        super().__init__('Surf Coast Marine')

    def extract_description(self, soup, features, list_page_data) -> str:
        # Step 1: Find the main section containing the description - in detailsTab
        details_tab = soup.find('div', id='detailsTab')
        description = ''
        if details_tab:
            # Step 2: Find the first <div> or <p> that contains the main textual description
            # There is a <p> that wraps a <div> and more <div>s below, but we just want boat description not the features/options
            desc_parts = []
            # Add the summary if present
            instock_summary = soup.find('p', class_='instock__summary')
            if instock_summary:
                desc_parts.append(instock_summary.get_text(separator=' ', strip=True))
            # Add the full description text up to the first <ul> (features start at the first <ul>)
            found = False
            for child in details_tab.find_all(['div','p'], recursive=True):
                if child.find('ul'):
                    break # Features/options start here so stop
                txt = child.get_text(separator=' ', strip=True)
                if txt and txt not in desc_parts and len(txt.split()) > 5:  # Filter out empty or very short text
                    desc_parts.append(txt)
            description = '\n\n'.join(desc_parts)
        return description.strip()

    def extract_image_urls(self, soup, features, list_page_data) -> list[str]:
        # Step 1: Locate the main gallery within the listing details
        gallery = soup.find('div', id='page_layout_page_template_pbAdvItemImageGallery1_pbAdvItemImageGallery1_ThumbPanel')
        image_urls = []
        if gallery:
            # Step 2: Find all <a> tags that link to images
            for a in gallery.find_all('a'):
                img_url = a.get('href')
                if img_url and img_url.startswith('/'):
                    # Convert to absolute URL
                    img_url = 'https://www.surfcoastmarine.com.au' + img_url
                if img_url and (img_url.endswith('.jpg') or img_url.endswith('.png') or img_url.endswith('.jpeg')):
                    image_urls.append(img_url)
        # Step 3: Remove duplicates
        image_urls = list(dict.fromkeys(image_urls))
        return image_urls
