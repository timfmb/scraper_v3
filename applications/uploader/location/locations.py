from applications.uploader.location.models import LocationValidationResponse
from interfaces.openai_client import OpenAIClient
from interfaces.scraper_db.locations.service import get_inferred_location, set_location
from logging_config import get_logger

logger = get_logger(__name__)



class Locationvalidator:
    def __init__(self):
        self.au_locations = [
            "New South Wales - Sydney & Surrounds",
            "New South Wales - North Coast",
            "New South Wales - South Coast",
            "Victoria - Melbourne & Port Phillip",
            "Victoria - Gippsland & East Coast",
            "Queensland - Brisbane & Gold Coast",
            "Queensland - Sunshine Coast & Fraser Coast",
            "Queensland - Whitsundays & Central Coast",
            "Queensland - Far North",
            "Western Australia - Perth & Fremantle",
            "Western Australia - South West",
            "Western Australia - North West",
            "South Australia - Adelaide & Gulf",
            "South Australia - Eyre Peninsula & West Coast",
            "Tasmania - Hobart & South",
            "Tasmania - North & East Coast",
            "Northern Territory - Darwin & Top End"
        ]

        self.nz_locations = [
            "Northland",
            "Auckland",
            "Waikato & Coromandel",
            "Bay of Plenty",
            "Hawke's Bay & Gisborne",
            "Taranaki",
            "Manawatū-Whanganui",
            "Wellington Region",
            "Nelson & Marlborough",
            "Tasman & West Coast",
            "Canterbury",
            "Otago",
            "Southland"    
        ]

        self.us_locations = [
            "Northeast - New England",
            "Northeast - Mid-Atlantic",
            "Southeast - Florida East Coast",
            "Southeast - Florida Gulf Coast",
            "Southeast - Carolinas & Georgia",
            "Gulf Coast - Alabama & Mississippi",
            "Gulf Coast - Louisiana",
            "Gulf Coast - Texas",
            "Great Lakes - Upper Midwest",
            "Great Lakes - Ohio & Pennsylvania",
            "Pacific Northwest - Washington",
            "Pacific Northwest - Oregon",
            "California - Northern",
            "California - Central",
            "California - Southern",
            "Alaska - Southcentral & Southeast",
            "Hawaii"
        ]


    def validate_location_openai(self, location: str, country: str) -> LocationValidationResponse:
        client = OpenAIClient()
        if country == 'New Zealand':
            with open('applications/uploader/location/prompts/nz_location.txt', 'r') as file:
                prompt = file.read()

        elif country == 'Australia':
            with open('applications/uploader/location/prompts/au_location.txt', 'r') as file:
                prompt = file.read()

        elif country == 'United States':
            with open('applications/uploader/location/prompts/us_location.txt', 'r') as file:
                prompt = file.read()

        response = client.openai_stuctured_request(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that validates the location of a boat."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": f"Location: {location}, Country: {country}"}
            ],
            response_format=LocationValidationResponse,
        )
        return response


    def validate_location(self, location: str, country: str) -> LocationValidationResponse:
        inferred_location = get_inferred_location(country, location)
        if inferred_location:
            if country == 'New Zealand' and inferred_location not in self.nz_locations:
                inferred_location = None
            elif country == 'Australia' and inferred_location not in self.au_locations:
                inferred_location = None
            elif country == 'United States' and inferred_location not in self.us_locations:
                inferred_location = None
            logger.debug(f'inferred location: {inferred_location}, country: {country}')
            return inferred_location, country

        validated_location = self.validate_location_openai(location, country)

        if validated_location['country_matched'] and validated_location['location']:
            set_location(country, location, validated_location['location'])
            return validated_location['location'], validated_location['country']
        return None, None