from pydantic import BaseModel
from datetime import datetime

class InferenceResult(BaseModel):
    boat_type: str | None
    hull_type: str | None
    style: str | None
    style_vector: list[float] | None
    boat_type_v2: str | None
    hull_type_v2: str | None
    style_v2: str | None
    style_vector_v2: list[float] | None

class InferredDescription(BaseModel):
    description: str | None
    original_description_hash: str | None


class ExtractedData(BaseModel):
    title: str | None
    status: str | None
    office: int | None
    length: float | None
    length_waterline: float | None
    beam: float | None
    draft: float | None
    year: int | None
    price: int | None
    currency: str | None
    part_share: str | None = None
    vat_status: bool | None
    location: str | None
    country: str | None
    make: str | None
    model: str | None
    make_model: str | None
    condition: str | None
    construction: str | None
    keel_type: str | None
    ballast: int | None
    displacement: int | None
    designer: str | None
    builder: str | None
    cabins: int | None
    berths: int | None
    heads: int | None
    boat_name: str | None
    range: int | None
    passenger_capacity: int | None
    engine_count: int | None
    fuel_type: str | None
    fuel_tankage: int | None
    engine_hours: int | None
    engine_power: int | None
    engine_manufacturer: str | None
    engine_model: str | None
    engine_location: str | None
    engine_drive_type: str | None
    maximum_speed: int | None
    cruising_speed: int | None
    prop_type: str | None
    description: str | None
    image_urls: list[str] | None
    image_download_urls: list[str|None] | None
    inference_result: InferenceResult | None = None
    validated_make: str | None = None
    validated_model: str | None = None
    inferred_description: InferredDescription | None = None


class Page(BaseModel):
    website_name: str
    url: str
    last_scraped: datetime | None = None
    html: str | None = None
    extracted_data: ExtractedData | None = None
    list_page_data: dict | None = None
    hash: str | None = None
    active: bool = True
    errors: list[str] | None = None
