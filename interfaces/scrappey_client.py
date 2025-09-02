import requests
from urllib.parse import urlparse

def get_proxy_object(proxy_url):
    parsed_url = urlparse(proxy_url)
    username = parsed_url.username
    password = parsed_url.password
    server = f"{parsed_url.scheme}://{parsed_url.hostname}:{parsed_url.port}"
    
    proxyObj = {
        "server": server,
        "username": username,
        "password": password
    }
    return proxyObj

def get_cookies_and_user_agent(api_key, target_url, proxy_url, version=126, browser_name='chrome'):
    url = f"https://publisher.scrappey.com/api/v1?key={api_key}"
    # url = f"http://localhost:87/v1?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "cmd": "request.get",
        "url": target_url,
        "proxy": proxy_url,
        "filter": ["cookieString", "userAgent"],
        "noDriver": True,
        "browser": [
            {
                "name": browser_name,
                "minVersion": version,
                "maxVersion": version
            }
        ]
    }
    
    if browser_name == 'firefox':
        body.pop('noDriver')
        
    print('----- Requesting cookies and user agent from Scrappey, may take 30 seconds -----')

    response = requests.post(url, json=body, headers=headers)
    
    try:
        response_data = response.json()
    except Exception as e:
        raise Exception('Error parsing response from Scrappey {}'.format(response.text))
    
    cookie_string = response_data['solution']['cookieString']  # Adjust this according to the actual response structure
    user_agent = response_data['solution']['userAgent']  # Adjust this according to the actual response structure
    cookie_object = parse_cookie_string(cookie_string, target_url=target_url)
    proxy_object = get_proxy_object(proxy_url)
    
    print('----- Cookies and user agent received from Scrappey -----')
    # print(f'User Agent: {user_agent}')
    # print(f'Cookies: {cookie_object}')
    
    return cookie_object, user_agent, proxy_object

def parse_cookie_string(cookie_string, target_url):
    # Extract domain from target URL
    parsed_url = urlparse(target_url)
    domain = parsed_url.netloc

    cookies = []
    print(cookie_string)
    for cookie in cookie_string.split('; '):
        try:
            name, value = cookie.split('=', 1)
            cookies.append({
                'name': name,
                'value': value,
                'domain': domain,
                'path': '/'
            })
        except Exception as e:
            continue
    return cookies



class ScrappeyClient:
    def __init__(self):
        self.base_url = 'https://api.scrappey.com/scrape'
        self.api_key = 'Cb3FhQUX08lP6uN9kw1KsxpkSUT2OH0Hok2X8Dpp5VSL3HRzFLHOWqanNeQS'


    def get_config(self, target_url, proxy, version=126, browser_name='chrome'):
        proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['server'].replace('http://', '')}"
        cookie_object, user_agent, proxy_obj = get_cookies_and_user_agent(self.api_key, target_url, proxy_url, version=version, browser_name=browser_name)
        print(cookie_object)
        print(user_agent)
        print(proxy_obj)
        return cookie_object, user_agent, proxy_obj