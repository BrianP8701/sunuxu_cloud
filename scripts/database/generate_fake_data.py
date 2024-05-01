# scripts/database/generate_fake_data.py
from faker import Faker
import random
from core.models import *
import datetime

from core.security import hash_password
from core.database import AzureSQLDatabase

db = AzureSQLDatabase()
fake = Faker()

def generate_property(user_id: int):

    return PropertyOrm(
        user_id=user_id,
        street_number=fake.building_number(),
        street_name=fake.street_name(),
        street_suffix=fake.street_suffix(),
        city=fake.city(),
        unit_number=fake.random_int(min=1, max=200),
        state=fake.state(),
        zip_code=fake.zipcode(),
        country=fake.country(),
        status=random.choice(['active', 'inactive']),
        type=random.choice(['residential', 'condo', 'coop', 'commercial', 'land', 'hoa', 'industrial', 'rental', 'other']),
        price=random.randint(50000, 1000000),
        mls_number=fake.random_number(digits=8),
        bedrooms=random.randint(1, 10),
        bathrooms=random.uniform(1, 10),
        floors=random.randint(1, 5),
        rooms=random.randint(1, 20),
        kitchens=random.randint(1, 5),
        families=random.randint(1, 5),
        lot_sqft=random.randint(500, 15000),
        built_year=random.randint(1900, 2021),
        list_start_date=fake.date_time_this_decade(),
        list_end_date=fake.date_time_this_decade(),
        expiration_date=fake.date_time_this_decade(),
        notes=fake.text(),
        description=fake.text(),
        attached_type=random.choice(['attached', 'semi_attached', 'detached']),
        section=fake.word(),
        school_district=fake.word(),
        pictures=[fake.image_url() for _ in range(random.randint(1, 5))],
        viewed=fake.date_time_this_decade()
    )

def generate_user(user_id, email):
    if random.random() < 0.5:
        middle_name = fake.first_name()
    else:
        middle_name = None
    
    return UserOrm(
        id=user_id,
        email=email,
        password=hash_password("p"),
        first_name=fake.first_name(),
        middle_name=middle_name,
        last_name=fake.last_name(),
        phone=fake.random_number(digits=10)
    )

def generate_person(user_id):
    return PersonOrm(
        user_id=user_id,
        first_name=fake.first_name(),
        middle_name=fake.first_name(),
        last_name=fake.last_name(),
        phone=fake.random_number(digits=10),  # Generates a random 10-digit number,
        email=fake.email(),
        
        notes=fake.text(),
        viewed=fake.date_time_this_decade(),

        status=random.choice(['active', 'inactive']),
        type=random.choice(['lead', 'prospect', 'client', 'past_client', 'agent', 'broker', 'attorney', 'other'])
    )

def generate_transaction(user_id):
    return TransactionOrm(
        user_id=user_id,
        type=random.choice(['sale', 'rent', 'lease', 'buy', 'other']),
        status=random.choice(['pending', 'closed', 'expired', 'withdrawn', 'off_market', 'other']),
        notes=fake.text(),
        viewed=fake.date_time_this_decade()

    )

def generate_participant(person_id, transaction_id):
    return ParticipantOrm(
        role=random.choice(['buyer', 'seller', 'buyer_agent', 'seller_agent', 'buyer_attorney', 'seller_attorney', 'buyer_agent_broker', 'seller_agent_broker']),
        notes=fake.text(),
        
        viewed=fake.date_time_this_decade()
    )

# Generate and add properties to session
if __name__ == "__main__":
    # For now we'll just make standalone objects, without any relationships
    number_of_people_to_generate = random.randint(100, 200)
    number_of_properties_to_generate = random.randint(100, 200)
    number_of_transactions_to_generate = random.randint(100, 200)

    user_id = 1
    email = "brian"

    user = generate_user(user_id, email)

    all_data = [user]

    for i in range(number_of_people_to_generate):
        print(f"Generating person {i}")
        person = generate_person(user_id)
        all_data.append(person)

    for i in range(number_of_properties_to_generate):
        print(f"Generating property {i}")
        property = generate_property(user_id)
        all_data.append(property)

    for i in range(number_of_transactions_to_generate):
        print(f"Generating transaction {i}")
        transaction = generate_transaction(user_id)
        all_data.append(transaction)

    print("Inserting all data")
    db.batch_insert(all_data)
    print("Done")
    db.dispose_instance()
