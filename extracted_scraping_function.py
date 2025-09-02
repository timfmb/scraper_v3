def scraping_function(soup) -> list[str]:
    # Step 1: Find the container that contains the boat listings (by id)
    container = soup.find('div', id='in-stock-boat-listings')
    if not container:
        return []
    # Step 2: Find each boat listing item within the container
    boat_items = container.find_all('div', class_='boat-listing-preview__item')
    urls = []
    # Step 3: For each boat listing, find the URL linking to the boat listing page
    for item in boat_items:
        # Within each item, find an <a> with class 'resource-title' and a href
        a = item.find('a', class_='resource-title')
        if a and a.has_attr('href'):
            url = a['href']
            # Convert relative URLs to absolute URLs
            if url.startswith('http://') or url.startswith('https://'):
                urls.append(url)
            elif url.startswith('/'):
                urls.append('https://www.surfcoastmarine.com.au' + url)
    # Step 4: Return the list of URLs
    return urls
