def scraping_function(soup) -> list[str]:
    # Step 1: Locate the container with all boat listings (div with class 'blog-layout-grid')
    container = soup.find('div', class_='blog-layout-grid')
    
    # Step 2: Within that container, find all <article> elements (each boat listing is an article)
    boat_articles = container.find_all('article') if container else []
    
    # Step 3: Initialize an empty list to store the boat listing URLs
    urls = []
    
    # Step 4: Iterate over each boat listing article
    for article in boat_articles:
        # Find the div with class 'entry-thumbnail' that holds the link
        thumb_div = article.find('div', class_='entry-thumbnail')
        if thumb_div:
            # Within the thumbnail div, find the <a> tag with an href attribute
            a_tag = thumb_div.find('a', href=True)
            if a_tag and a_tag['href'].startswith(('http://', 'https://')):
                # Step 5: Append the URL to our list
                urls.append(a_tag['href'])
    
    # Step 6: Return the complete list of boat listing URLs
    return urls
