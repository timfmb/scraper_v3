


def extract_country(string):
    countries = ['Andorra', 'Afghanistan', 'Antigua and Barbuda', 'Albania', 'Armenia', 'Angola', 'Argentina', 'Austria', 'Australia', 'Azerbaijan', 'Barbados', 'Bangladesh', 'Belgium', 'Burkina Faso', 'Bulgaria', 'Bahrain', 'Burundi', 'Benin', 'Brunei Darussalam', 'Bolivia', 'Brazil', 'Bahamas', 'Bhutan', 'Botswana', 'Belarus', 'Belize', 'Canada', 'Democratic Republic of the Congo', 'Republic of the Congo', "CÃ´te d'Ivoire", 'Chile', 'Cameroon', "People's Republic of China", 'Colombia', 'Costa Rica', 'Cuba', 'Cape Verde', 'Cyprus', 'Czech Republic', 'Germany', 'Djibouti', 'Denmark', 'Dominica', 'Dominican Republic', 'Ecuador', 'Estonia', 'Egypt', 'Eritrea', 'Ethiopia', 'Finland', 'Fiji', 'France', 'Gabon', 'Georgia', 'Ghana', 'The Gambia', 'Guinea', 'Greece', 'Guatemala', 'Haiti', 'Guinea-Bissau', 'Guyana', 'Honduras', 'Hungary', 'Indonesia', 'Republic of Ireland', 'Israel', 'India', 'Iraq', 'Iran', 'Iceland', 'Italy', 'Ireland', 'Jamaica', 'Jordan', 'Japan', 'Kenya', 'Kyrgyzstan', 'Kiribati', 'North Korea', 'South Korea', 'Kuwait', 'Lebanon', 'Liechtenstein', 'Liberia', 'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia', 'Libya', 'Madagascar', 'Marshall Islands', 'Macedonia', 'Mali', 'Myanmar', 'Mongolia', 'Mauritania', 'Malta', 'Mauritius', 'Maldives', 'Malawi', 'Mexico', 'Malaysia', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Nicaragua', 'Kingdom of the Netherlands', 'The Netherlands', 'Netherlands', 'Norway', 'Nepal', 'Nauru', 'New Zealand', 'Oman', 'Panama', 'Peru', 'Papua New Guinea', 'Philippines', 'Pakistan', 'Poland', 'Portugal', 'Palau', 'Paraguay', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saudi Arabia', 'Solomon Islands', 'Seychelles', 'Sudan', 'Sweden', 'Singapore', 'Slovenia', 'Slovakia', 'Sierra Leone', 'San Marino', 'Senegal', 'Somalia', 'Suriname', 'SÃ£o TomÃ© and PrÃ\xadncipe', 'Syria', 'Togo', 'Thailand', 'Tajikistan', 'Turkmenistan', 'Tunisia', 'Tonga', 'Turkey', 'Trinidad and Tobago', 'Tuvalu', 'Tanzania', 'Ukraine', 'Uganda', 'United States', 'Uruguay', 'Uzbekistan', 'Vatican City', 'Venezuela', 'Vietnam', 'Vanuatu', 'Yemen', 'Zambia', 'Zimbabwe', 'Algeria', 'Bosnia and Herzegovina', 'Cambodia', 'Central African Republic', 'Chad', 'Comoros', 'Croatia', 'East Timor', 'El Salvador', 'Equatorial Guinea', 'Grenada', 'Kazakhstan', 'Laos', 'Federated States of Micronesia', 'Moldova', 'Monaco', 'Montenegro', 'Morocco', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'Serbia', 'South Africa', 'Spain', 'Sri Lanka', 'Swaziland', 'Switzerland', 'United Arab Emirates', 'United Kingdom']
    usa_state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
    usa_state_abbrev = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    

    countrey_abbrevs = {
        'usa': 'United States',
        'uk': 'United Kingdom',
        'uae': 'United Arab Emirates',
        "bvi": "British Virgin Islands",
    }

    cities_dict = {
        'mallorca': 'Spain',
        'majorca': 'Spain',
        'ibiza': 'Spain',
        'menorca': 'Spain',
        'formentera': 'Spain',
        'barcelona': 'Spain',
        'madrid': 'Spain',
        'valencia': 'Spain',
        'seville': 'Spain',
        'alicante': 'Spain',
        'malaga': 'Spain',
        'marbella': 'Spain',
        'costa del sol': 'Spain',
        'costa brava': 'Spain',
        'costa blanca': 'Spain',
        'Athens': 'Greece',
        'corfu': 'Greece',
        'crete': 'Greece',
        'mykonos': 'Greece',
        "Guadeloupe": "France",
        "pula": "Croatia",
        "nassau": "Bahamas",
        "fethiye": "Turkey",
        "antigua": "Antigua and Barbuda",
        "cote d'azur": "France",
        "la paz": "Mexico",
        "sibenik": "Croatia",
        "trogir": "Croatia",
        "lavrion": "Greece",
        "sicily": "Italy",
        "St. Martin": "Sint Maarten",
        "French Atlantic": "France",
        "Dubrovnik": "Croatia",
        "Marseille": "France",
        "Raiatea": "French Polynesia",
        "Placencia": "Belize",
        "Corsica": "France",
        "Martinique": "France",
        "Olbia": "Italy",
        "Kotor": "Montenegro",
        "Lefkas": "Greece",
        "Whitsundays": "Australia",
        "Kos": "Greece",
        "Gocek": "Turkey",
        "Istanbul": "Turkey",
        "Sint Maarten": "Sint Maarten",
        "Cancun": "Mexico",
        "Marmaris": "Turkey",
        "Fajardo": "Puerto Rico",
        "Buenaventura": "Colombia",
        "Abu Dhabi": "United Arab Emirates",
        "Bodrum": "Turkey",
        "Izmir": "Turkey",
        "Basse-Terre": "France",
        "Papeete": "French Polynesia",
        "Saint George": "Grenada",
        "Sliema": "Malta",
        "Bridgetown": "Barbados",
        "Naples": "Italy",
        "Ontario": "Canada",
        "Glyfada": "Greece",
        "Cannes": "France",
        "Napoli": "Italy",
        "Genova": "Italy",
        "FREJUS": "France",
        "Port Adriano": "Spain",
        "Palma": "Spain",
        "Chioggia": "Italy",
        "Empuriabrava": "Spain",
        "Antibes": "France",
        "A Coruna": "Spain",
        "budoni": "Italy",
        "Sainte-Maxime": "France",
        "Athene": "Greece",
        "La Spezia": "Italy",
        "Mahon": "Spain",
        "Sotogrande": "Spain",
        "Loano": "Italy",
        "Savona": "Italy",
        "Varazze": "Italy",
        "Hong Kong": "Hong Kong",
    }

    for country in countries:
        if country in string:
            return country
        
    for state in usa_state_names:
        if state in string:
            return 'United States'
        
    for abbrev in countrey_abbrevs:
        if abbrev.lower() in string.lower():
            return countrey_abbrevs[abbrev]
        
    if 'dubai' in string.lower():
        return 'United Arab Emirates'
        

    for city in cities_dict:
        if city.lower() in string.lower():
            return cities_dict[city]
    

    for state in usa_state_abbrev:
        if state in string:
            return 'United States'
        