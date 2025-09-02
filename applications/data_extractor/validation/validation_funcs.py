


def title(listing):
    title = listing.get('title')
    if not title:
        return False
    return True


def status(listing):
    status = listing.get('status')
    if not status:
        return False
    
    if status not in ['Available', 'Under Offer', 'Sale Pending']:
        return False
    
    return True


def office(listing):
    office = listing.get('office')
    if not office:
        return False
    return True


def length(listing):
    length = listing.get('length')
    if not length:
        return False
    
    if length < 1 or length > 200:
        return False

    return True



def length_waterline(listing):
    length_waterline = listing.get('length_waterline')
    if not length_waterline:
        return False
    
    if length_waterline < 1 or length_waterline > 200:
        return False

    return True


def beam(listing):
    beam = listing.get('beam')
    if not beam:
        return False
    
    if beam < 0.3 or beam > 50:
        return False

    return True



def draft(listing):
    draft = listing.get('draft')
    if not draft:
        return False
    
    if draft < 0.3 or draft > 50:
        return False

    return True



def year(listing):
    year = listing.get('year')
    if not year:
        return False
    
    if year < 1800 or year > 2028:
        return False

    return True



def price(listing):
    price = listing.get('price')
    if not price:
        return False
    
    if price < 0 or price > 1_000_000_000:
        return False

    return True


def currency(listing):
    currency = listing.get('currency')
    if not currency:
        return False
    
    if len(currency) != 3:
        return False

    return True



def vat_status(listing):
    vat_status = listing.get('vat_status')
    if not vat_status:
        return False
    
    if vat_status not in [True, False, None]:
        return False

    return True



def location(listing):
    location = listing.get('location')
    if not location:
        return False
    return True



def country(listing):
    country = listing.get('country')
    if not country:
        return False
    return True



def make(listing):
    make = listing.get('make')
    if not make:
        return False
    return True


def model(listing):
    model = listing.get('model')
    if not model:
        return False
    return True


def make_model(listing):
    make_model = listing.get('make_model')
    if not make_model:
        return False
    return True


def condition(listing):
    condition = listing.get('condition')
    if not condition:
        return False
    
    if condition not in ['New', 'Used']:
        return False

    return True


def boat_type(listing):
    boat_type = listing.get('boat_type')
    if not boat_type:
        return False
    
    if boat_type not in ['Sail', 'Power']:
        return False

    return True


def category(listing):
    category = listing.get('category')
    if not category:
        return False

    return True


def construction(listing):
    construction = listing.get('construction')
    if not construction:
        return False

    return True


def keel_type(listing):
    keel_type = listing.get('keel_type')
    if not keel_type:
        return False

    return True


def ballast(listing):
    ballast = listing.get('ballast')
    if not ballast:
        return False

    return True


def displacement(listing):
    displacement = listing.get('displacement')
    if not displacement:
        return False

    return True


def designer(listing):
    designer = listing.get('designer')
    if not designer:
        return False

    return True


def builder(listing):
    builder = listing.get('builder')
    if not builder:
        return False

    return True


def cabins(listing):
    cabins = listing.get('cabins')
    if not cabins:
        return False

    return True


def berths(listing):
    berths = listing.get('berths')
    if not berths:
        return False

    return True



def heads(listing):
    heads = listing.get('heads')
    if not heads:
        return False

    return True


def boat_name(listing):
    boat_name = listing.get('boat_name')
    if not boat_name:
        return False

    return True


def range(listing):
    range = listing.get('range')
    if not range:
        return False

    return True


def passenger_capacity(listing):
    passenger_capacity = listing.get('passenger_capacity')
    if not passenger_capacity:
        return False

    return True


def engine_count(listing):
    engine_count = listing.get('engine_count')
    if not engine_count:
        return False

    return True


def fuel_type(listing):
    fuel_type = listing.get('fuel_type')
    if not fuel_type:
        return False

    return True


def fuel_tankage(listing):
    fuel_tankage = listing.get('fuel_tankage')
    if not fuel_tankage:
        return False

    return True


def engine_hours(listing):
    engine_hours = listing.get('engine_hours')
    if not engine_hours:
        return False

    return True


def engine_power(listing):
    engine_power = listing.get('engine_power')
    if not engine_power:
        return False

    return True


def engine_manufacturer(listing):
    engine_manufacturer = listing.get('engine_manufacturer')
    if not engine_manufacturer:
        return False

    return True


def engine_model(listing):
    engine_model = listing.get('engine_model')
    if not engine_model:
        return False

    return True


def engine_location(listing):
    engine_location = listing.get('engine_location')
    if not engine_location:
        return False

    return True


def drive_type(listing):
    drive_type = listing.get('drive_type')
    if not drive_type:
        return False

    return True


def maximum_speed(listing):
    maximum_speed = listing.get('maximum_speed')
    if not maximum_speed:
        return False

    return True


def cruising_speed(listing):
    cruising_speed = listing.get('cruising_speed')
    if not cruising_speed:
        return False

    return True


def propeller_type(listing):
    propeller_type = listing.get('propeller_type')
    if not propeller_type:
        return False

    return True


def description(listing):
    description = listing.get('description')
    if not description:
        return False

    return True


def image_urls_exists(listing):
    image_urls = listing.get('image_urls')
    if not image_urls:
        return False
    return True
    
    
def image_download_urls_not_none(listing):
    image_urls = listing.get('image_urls')
    image_download_urls = listing.get('image_download_urls')
    if None in image_download_urls or len(image_download_urls) != len(image_urls):
        return False

    return True
