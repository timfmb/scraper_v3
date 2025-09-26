from ..client import get_db


def get_collection():
    db = get_db()
    return db['locations']


def set_location(country: str, location: dict, inferred_location: str):
    collection = get_collection()
    collection.insert_one({'country': country, 'location': location, 'inferred_location': inferred_location})


def get_inferred_location(country: str, location: dict):
    collection = get_collection()
    loc = collection.find_one({'country': country, 'location': location}, {'inferred_location': 1})
    if loc:
        return loc['inferred_location']
    return None


def get_all_locations():
    collection = get_collection()
    return collection.find({}, {})


def remove_location(country: str, location: dict):
    collection = get_collection()
    collection.delete_one({'country': country, 'location': location})
