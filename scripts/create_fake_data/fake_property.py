from typing import Dict, Any, List
from faker import Faker
from core.enums import PropertyType, PropertyAttachedType, State

fake = Faker()

def fake_property_data(
    user_ids: List[int], owner_ids: List[int], occupant_ids: List[int]
) -> Dict[str, Any]:
    """
    Generates a dictionary of property data using Faker.

    :return:
        A dictionary containing the property details.
    """
    return {
        "user_ids": user_ids,
        "owner_ids": owner_ids,
        "occupant_ids": occupant_ids,
        "street_number": fake.building_number(),
        "street_name": fake.street_name(),
        "street_suffix": fake.street_suffix(),
        "city": fake.city(),
        "state": fake.random_element(elements=State).value,
        "zip_code": fake.zipcode(),
        "country": fake.country(),
        "unit": fake.secondary_address() if fake.boolean() else None,
        "mls_number": fake.bothify(text='MLS-#####') if fake.boolean() else None,
        "type": fake.random_element(elements=PropertyType).value,
        "google_place_id": fake.bothify(text='G-##########') if fake.boolean() else None,
        "mls": fake.bothify(text='MLS-###') if fake.boolean() else None,
        "bedrooms": fake.random_int(min=1, max=10),
        "bathrooms": fake.random_int(min=1, max=10),
        "floors": fake.random_int(min=1, max=5),
        "rooms": fake.random_int(min=1, max=20),
        "kitchens": fake.random_int(min=1, max=3),
        "families": fake.random_int(min=1, max=3),
        "lot_sqft": fake.random_int(min=500, max=10000),
        "building_sqft": fake.random_int(min=500, max=10000),
        "year_built": fake.year(),
        "list_start_date": fake.date_time_this_decade(),
        "list_end_date": fake.date_time_this_decade(),
        "expiration_date": fake.date_time_this_decade(),
        "attached_type": fake.random_element(elements=PropertyAttachedType).value,
        "section": fake.word() if fake.boolean() else None,
        "school_district": fake.word() if fake.boolean() else None,
        "property_tax": fake.random_number(digits=5, fix_len=True) / 100,
        "pictures": [fake.image_url() for _ in range(fake.random_int(min=1, max=5))],
        "notes": fake.text(max_nb_chars=200),
        "description": fake.text(max_nb_chars=500),
    }
