import requests



class WebshareClient:
    def __init__(self) -> None:
        self.base_url = "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=100"
        self.api_key = 'xcki07ccrdiiqg6gxzbilj846wt19drps9jct2ee'

    
    def list_proxies(self):
        response = requests.get(self.base_url, headers={'Authorization': f'Token {self.api_key}'})
        
        results = response.json()['results']

        proxies = []

        for result in results:
            address = result['proxy_address']
            port = result['port']
            username = result['username']
            password = result['password']

            proxy = f"{address}:{port}"
            proxies.append({
                'server': f'http://{proxy}',
                'username': username,
                'password': password
            })

        return proxies