from typing import List, Optional
from pydantic import BaseModel


class OutputCleanDescription(BaseModel):
    description: str


class BoatListing(BaseModel):
    title: str
    status: str
    url: str
    office: Optional[int|None]
    length: Optional[float|None]
    length_waterline: Optional[float|None]
    beam: Optional[float|None]
    draft: Optional[float|None]
    year: Optional[int|None]
    price: Optional[int|None]
    currency: Optional[str|None]
    vat_status: Optional[bool|None]
    location: Optional[str|None]
    country: Optional[str|None]
    search_location: Optional[str|None]
    make: Optional[str|None]
    model: Optional[str|None]
    make_model: Optional[str|None]
    condition: Optional[str|None]
    construction: Optional[str|None]
    keel_type: Optional[str|None]
    ballast: Optional[float|None]
    displacement: Optional[float|None]
    designer: Optional[str|None]
    builder: Optional[str|None]
    cabins: Optional[int|None]
    berths: Optional[int|None]
    heads: Optional[int|None]
    boat_name: Optional[str|None]
    range: Optional[int|None]
    passenger_capacity: Optional[int|None]
    engine_count: Optional[int|None]
    fuel_type: Optional[str|None]
    fuel_tankage: Optional[int|None]
    engine_hours: Optional[int|None]
    engine_power: Optional[int|None]
    engine_manufacturer: Optional[str|None]
    engine_model: Optional[str|None]
    engine_location: Optional[str|None]
    engine_drive_type: Optional[str|None]
    maximum_speed: Optional[int|None]
    cruising_speed: Optional[int|None]
    prop_type: Optional[str|None]
    description: Optional[str|None]
    broker: Optional[str|None]
    boat_type_v2: Optional[str|None]
    hull_type_v2: Optional[str|None]
    style_v2: Optional[str|None]
    style_vector_v2: Optional[List[float]]
    images: List[str|None]
    image_url: Optional[str|None]
    price_usd: Optional[int|None]
    validated_make: Optional[str|None]
    validated_model: Optional[str|None]

