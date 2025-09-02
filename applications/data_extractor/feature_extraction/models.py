from pydantic import BaseModel

class BrokerDetails(BaseModel):
    name: str | None
    email: str | None
    phone: str | None
    mobile: str | None


class Output(BaseModel):
    PRICE_DETAILS: int | None
    CURRENCY_DETAILS: str | None
    VAT_STATUS_DETAILS: bool | None
    LENGTH_DETAILS: float | None
    LENGTH_WATERLINE_DETAILS: float | None
    BEAM_DETAILS: float | None
    DRAFT_DETAILS: float | None
    YEAR_DETAILS: int | None
    LOCATION_DETAILS: str | None
    COUNTRY_DETAILS: str | None
    MAKE_DETAILS: str | None
    MODEL_DETAILS: str | None
    CONDITION_DETAILS: str | None
    CONSTRUCTION_DETAILS: str | None
    DISPLACEMENT_DETAILS: float | None
    DESIGNER_DETAILS: str | None
    BUILDER_DETAILS: str | None
    CABINS_DETAILS: int | None
    BERTHS_DETAILS: int | None
    HEADS_DETAILS: int | None
    RANGE_DETAILS: int | None
    PASSENGER_CAPACITY_DETAILS: int | None
    ENGINE_COUNT_DETAILS: int | None
    FUEL_TYPE_DETAILS: str | None
    FUEL_TANK_SIZE_DETAILS: int | None
    ENGINE_HOURS_DETAILS: int | None
    ENGINE_POWER_DETAILS: int | None
    ENGINE_MANUFACTURER_DETAILS: str | None
    ENGINE_MODEL_DETAILS: str | None
    ENGINE_LOCATION_DETAILS: str | None
    ENGINE_DRIVE_TYPE_DETAILS: str | None
    MAXIMUM_SPEED_DETAILS: int | None
    CRUISING_SPEED_DETAILS: int | None
    PROP_TYPE_DETAILS: str | None
    PROP_COUNT_DETAILS: int | None
    BROKER_DETAILS: BrokerDetails | None