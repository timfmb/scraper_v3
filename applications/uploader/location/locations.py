from applications.uploader.location.models import LocationValidationResponse
from interfaces.openai_client import OpenAIClient
from interfaces.scraper_db.locations.service import get_inferred_location, set_location



class Locationvalidator:
    def __init__(self):
        pass


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
            return inferred_location, country

        validated_location = self.validate_location_openai(location, country)

        if validated_location['country_matched'] and validated_location['location']:
            set_location(country, location, validated_location['location'])
            return validated_location['location'], validated_location['country']
        return None, None