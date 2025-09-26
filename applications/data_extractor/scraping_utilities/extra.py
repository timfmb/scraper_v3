import re


def extract_fuel_tank_size(text):
    # Define regular expressions for fuel tank sizes in liters, gallons, and any other common units
    liter_pattern = re.compile(r'(\d{1,3}(?:,\d{3})*|\d+\.?\d*)\s*(liters?|l)\b', re.IGNORECASE)
    gallon_pattern = re.compile(r'(\d{1,3}(?:,\d{3})*|\d+\.?\d*)\s*(gallons?|gal)\b', re.IGNORECASE)
    
    # Try to find a match for liters
    liter_match = liter_pattern.search(text)
    if liter_match:
        # Remove commas for conversion
        liters = float(liter_match.group(1).replace(',', ''))
        return liters

    # Try to find a match for gallons if no liter match is found
    gallon_match = gallon_pattern.search(text)
    if gallon_match:
        # Remove commas for conversion
        gallons = float(gallon_match.group(1).replace(',', ''))
        liters = gallons * 3.78541  # Convert gallons to liters
        return liters

    # If no matches were found, return None or raise an exception
    return None





def extract_engine_manufacturer(string):
    manufacturers = [
        "daimler-benz",
        "caterpillar",
        "thornycroft",
        "volvo penta",
        "westerbeake",
        "betamarine",
        "john deere",
        "lombardini",
        "mercruiser",
        "mitsubishi",
        "westerbeke",
        "aquapella",
        "covington",
        "oceanvolt",
        "universal",
        "volkwagen",
        "chrysler",
        "crusader",
        "daihatsu",
        "evinrude",
        "hercules",
        "kawasaki",
        "mercedes",
        "michigan",
        "sullivan",
        "cummins",
        "detroit",
        "gardner",
        "johnson",
        "kermath",
        "mariner",
        "mercury",
        "perkins",
        "tohatsu",
        "daewoo",
        "ivecco",
        "kubota",
        "lehman",
        "lister",
        "lugger",
        "perama",
        "suzuki",
        "toyota",
        "verado",
        "yamaha",
        "yanmar",
        "bravo",
        "dusan",
        "honda",
        "ilmor",
        "iveco",
        "izuzu",
        "nanni",
        "penta",
        "rotax",
        "sabre",
        "vetus",
        "weber",
        "volvo",
        "beta",
        "ford",
        "hino",
        "kota",
        "bmc",
        "man",
        "mtu",
        "pcm",
        "gm"
    ]

    for manufacturer in manufacturers:
        if manufacturer in string.lower():
            return manufacturer.title()
        

