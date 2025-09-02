
deduplication_dict = {
  "US": "United States",
  "USA": "United States",
  "United States of America": "United States",
  "United States Of America": "United States",
  
  "Great Britain": "United Kingdom",
  "England": "United Kingdom",
  
  "Türkiye": "Turkey",
  "Turkey or Greece": "Turkey",
  "Turkey / Greece": "Turkey",
  
  "The Netherlands": "Netherlands",
  "Netherlands Antilles": "Netherlands",
  
  "Hong Kong SAR China": "Hong Kong",
  
  "Republic of Cyprus": "Cyprus",
  
  "St Kitts and Nevis": "Saint Kitts and Nevis",
  
  "Saint Martin": "Saint Martin (French part)",
  "Sint Maarten": "Saint Martin (Dutch part)",
  
  "Virgin Islands (British)": "British Virgin Islands",
  "United States Virgin Islands": "United States Virgin Islands",
  
  "Kaimaninseln": "Cayman Islands",
  
  "French Polynesia / Fiji": "French Polynesia",
  
  "Spain or Dominican Republic": "Spain",
  
  "Korea": "South Korea",
  
  "Unknown": "Unknown",
  "Not Available": "Unknown",
  "null": "Unknown",
  
  "Northern Europe": "Europe",
  "Mediterranean Sea region": "Europe",
  "Multiple - Europe (available in Mediterranean)": "Europe",
  "Africa": "Africa",
  "South Pacific": "South Pacific",
  "Caribbean": "Caribbean",
  "International Waters": "International Waters"
}

def clean_country(country: str) -> str:
    if country in deduplication_dict:
        return deduplication_dict[country]
    return country
    