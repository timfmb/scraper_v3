from diskcache import Cache
import requests
from time import time


class CurrencyConverter:
    def __init__(self):
        self.cache = Cache('currency_cache')

    

    def get_rates(self):
        url = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_ENzYY5h2n2IX22mfNkXtB5gPCpusoGOMDQtaj5Yv&currencies="
        response = requests.get(url)
        results = response.json().get('data')
        self.cache.set('rates_to_usd', results)
        self.cache.set('last_updated', time())
        return results
    


    def check_cache(self):
        last_updated = self.cache.get('last_updated')
        if not last_updated:
            return self.get_rates()
        
        if time() - last_updated > 86400:
            return self.get_rates()



    def convert_to_usd(self, amount, currency):
        self.check_cache()
        rates = self.cache.get('rates_to_usd')
        
        if currency == 'USD':
            return amount
        
        if rates.get(currency):
            return amount / rates[currency]
        
        return None
        
