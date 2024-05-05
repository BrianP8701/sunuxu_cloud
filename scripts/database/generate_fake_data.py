# scripts/database/generate_fake_data.py
from faker import Faker
import random
from core.models import *
import asyncio

from core.security import hash_password
from core.database import AzurePostgreSQLDatabase

db = AzurePostgreSQLDatabase()
fake = Faker()

def generate_property(user_id: int):

    return PropertyOrm(
        user_id=user_id,
        street_number=fake.building_number(),
        street_name=fake.street_name(),
        street_suffix=fake.street_suffix(),
        city=fake.city(),
        unit_number=str(fake.random_int(min=1, max=200)),
        state=fake.state(),
        zip_code=fake.zipcode(),
        country=fake.country(),
        status=random.choice(['active', 'inactive']),
        type=random.choice(['residential', 'condo', 'coop', 'commercial', 'land', 'hoa', 'industrial', 'rental', 'other']),
        price=random.randint(50000, 1000000),
        mls_number=str(fake.random_number(digits=8)),
        bedrooms=random.randint(1, 10),
        bathrooms=random.uniform(1, 10),
        floors=random.randint(1, 5),
        rooms=random.randint(1, 20),
        kitchens=random.randint(1, 5),
        families=random.randint(1, 5),
        lot_sqft=random.randint(500, 15000),
        building_sqft=random.randint(500, 15000),
        year_built=random.randint(1900, 2021),
        list_start_date=fake.date_time_this_decade(),
        list_end_date=fake.date_time_this_decade(),
        expiration_date=fake.date_time_this_decade(),
        notes=fake.text(),
        description=fake.text(),
        attached_type=random.choice(['attached', 'semi_attached', 'detached']),
        section=fake.word(),
        school_district=fake.word(),
        property_tax=random.uniform(0, 10000),
        pictures=str([fake.image_url() for _ in range(random.randint(1, 5))]),
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
        phone=str(fake.random_number(digits=10))  # Generates a random 10-digit number,
    )

def generate_person(user_id):
    return PersonOrm(
        user_id=user_id,
        first_name=fake.first_name(),
        middle_name=fake.first_name(),
        last_name=fake.last_name(),
        phone=str(fake.random_number(digits=10)),  # Generates a random 10-digit number,
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
    async def main():
        user_id = 1
        email = "brian@example.com"
        user = generate_user(user_id, email)

        await db.insert(user)

        all_people = [generate_person(user_id) for _ in range(random.randint(100, 200))]
        all_properties = [generate_property(user_id) for _ in range(random.randint(100, 200))]
        all_transactions = [generate_transaction(user_id) for _ in range(random.randint(100, 200))]

        await db.batch_insert(all_people)
        await db.batch_insert(all_properties)
        await db.batch_insert(all_transactions)
        await db.dispose_instance()

    asyncio.run(main())