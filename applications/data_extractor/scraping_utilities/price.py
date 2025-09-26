
import re
from unidecode import unidecode


def extract_price_by_removing_non_numeric(text):
    text = unidecode(text)
    numeric_string = re.sub(r'[^0-9]', '', text)
    return int(numeric_string)




def extract_price_and_currency(text):

    currencies = [
        'USD',  # US Dollar
        'EUR',  # Euro
        'GBP',  # British Pound
        'JPY',  # Japanese Yen
        'INR',  # Indian Rupee
        'KRW',  # South Korean Won
        'RUB',  # Russian Ruble
        'TRY',  # Turkish Lira
        'BRL',  # Brazilian Real
        'CAD',  # Canadian Dollar
        'AUD',  # Australian Dollar
        'NZD',  # New Zealand Dollar
        'CHF',  # Swiss Franc
        'HKD',  # Hong Kong Dollar
        'SGD',  # Singapore Dollar
        'SEK',  # Swedish Krona
        'DKK',  # Danish Krone
        'PLN',  # Polish Zloty
        'HUF',  # Hungarian Forint
        'ILS',  # Israeli Shekel
        'THB',  # Thai Baht
        'ZAR',  # South African Rand
        'NGN',  # Nigerian Naira
        'CZK',  # Czech Koruna
        'VND',  # Vietnamese Dong
        'PHP',  # Philippine Peso
        'BTC',  # Bitcoin (Cryptocurrency)
        'ETH'  # Ethereum (Cryptocurrency)
    ]

    currency_map = {
        "$": "USD",  # US Dollar
        "€": "EUR",  # Euro
        "£": "GBP",  # British Pound
        "¥": "JPY",  # Japanese Yen
        "₹": "INR",  # Indian Rupee
        "₩": "KRW",  # South Korean Won
        "₽": "RUB",  # Russian Ruble
        "₺": "TRY",  # Turkish Lira
        "R$": "BRL",  # Brazilian Real
        "C$": "CAD",  # Canadian Dollar
        "A$": "AUD",  # Australian Dollar
        "NZ$": "NZD",  # New Zealand Dollar
        "CHF": "CHF",  # Swiss Franc
        "HK$": "HKD",  # Hong Kong Dollar
        "S$": "SGD",  # Singapore Dollar
        "kr": "SEK",  # Swedish Krona
        "kr.": "DKK",  # Danish Krone
        "zł": "PLN",  # Polish Zloty
        "Ft": "HUF",  # Hungarian Forint
        "₪": "ILS",  # Israeli Shekel
        "฿": "THB",  # Thai Baht
        "R": "ZAR",  # South African Rand
        "₦": "NGN",  # Nigerian Naira
        "Kč": "CZK",  # Czech Koruna
        "₫": "VND",  # Vietnamese Dong
        "₱": "PHP",  # Philippine Peso
        "฿": "BTC",  # Bitcoin (Cryptocurrency)
        "Ξ": "ETH"  # Ethereum (Cryptocurrency)
    }

    found_currency = None

    for currency in currencies:
        if currency in text:
            found_currency = currency
            break

    # Regular expression to match a currency symbol followed by a price
    pattern = r'([$€£¥₹])\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    match = re.search(pattern, text)
    
    if match:
        symbol = match.group(1)
        price_str = match.group(2)
        
        # Remove any commas from the price string and convert to an integer
        price = int(float(price_str.replace(',', '')))
        
        
        if not found_currency:
            # Get the currency code from the symbol
            currency = currency_map.get(symbol, None)  # UNK for unknown currency
            
            return price, currency
        else:
            return price, found_currency
    
    return None, None
