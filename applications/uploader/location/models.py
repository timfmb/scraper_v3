from pydantic import BaseModel


class LocationValidationResponse(BaseModel):
    country: str
    location: str
    country_matched: bool