import asyncio
from core.database.azure_postgresql import AzurePostgreSQLDatabase
from core.models import *
from core.utils.search import search
from core.security import hash_password
import faker

fake = faker.Faker()
user_id = 2

async def main():
    db = AzurePostgreSQLDatabase()
    
    # Insert test data
    email = "testuser@example.com"
    user = UserOrm(
        id=user_id,
        email=email,
        password=hash_password("password"),
        first_name="Test",
        middle_name="Middle",
        last_name="User",
        phone="1234567890"
    )
    await db.insert(user)

    person = PersonOrm(
        user_id=user_id,
        first_name="UniqueFirstName",
        middle_name="UniqueMiddleName",
        last_name="UniqueLastName",
        notes="Some notes",
        language="English"
    )
    await db.insert(person)
    person_row = PersonRowOrm(
        user_id=user_id,
        id=person.id,
        name="UniqueFirstName UniqueMiddleName UniqueLastName",
        type="client",
        active=True,
        viewed=fake.date_time_this_decade()
    )
    await db.insert(person_row)

    property = PropertyOrm(
        user_id=user_id,
        street_number="123",
        street_name="UniqueStreet",
        street_suffix="Ave",
        city="UniqueCity",
        unit="1",
        state="UniqueState",
        zip_code="12345",
        country="UniqueCountry",
        bedrooms=3,
        bathrooms=2.5,
        floors=2,
        rooms=5,
        kitchens=1,
        families=1,
        lot_sqft=1000,
        building_sqft=2000,
        year_built=2000,
        list_start_date=fake.date_time_this_decade(),
        list_end_date=fake.date_time_this_decade(),
        expiration_date=fake.date_time_this_decade(),
        google_place_id=fake.uuid4(),
        notes="Property notes",
        description="Property description",
        attached_type="detached",
        section="Section",
        school_district="District",
        property_tax=1000.0,
        pictures="[]"
    )
    await db.insert(property)
    property_row = PropertyRowOrm(
        user_id=user_id,
        id=property.id,
        address="123 UniqueStreet Ave, UniqueCity, UniqueState, 12345",
        mls_number="12345678",
        active=True,
        type="residential",
        price=500000,
        viewed=fake.date_time_this_decade()
    )
    await db.insert(property_row)

    transaction = TransactionOrm(
        user_id=user_id,
        description="Transaction description",
        notes="Transaction notes"
    )
    await db.insert(transaction)
    transaction_row = TransactionRowOrm(
        user_id=user_id,
        id=transaction.id,
        name="UniqueTransactionName",
        status="pending",
        type="sell",
        viewed=fake.date_time_this_decade()
    )
    await db.insert(transaction_row)

    # Test cases
    print("Testing people search by name...")
    results = await search("people", "UniqueFirstName", user_id)
    print(f"Results: {results}")

    print("Testing people search by name typo...")
    results = await search("people", "UnifueFirstName UniqueMiddleName UniqueLastName", user_id)
    print(f"Results: {results}")

    print("Testing property search by address...")
    results = await search("properties", "123 UniqueStreet Ave", user_id)
    print(f"Results: {results}")
    
    print("Testing property search by address typo...")
    results = await search("properties", "123 UniqueStreet Av", user_id)
    print(f"Results: {results}")

    print("Testing property search by MLS number...")
    results = await search("properties", "12345678", user_id)
    print(f"Results: {results}")

    print("Testing transaction search by name...")
    results = await search("transactions", "UniqueTransactionName", user_id)
    print(f"Results: {results}")

    print("Testing transaction search by name typo...")
    results = await search("transactions", "UniqueTransactinName", user_id)
    print(f"Results: {results}")

    # Cleanup
    await db.delete(UserOrm, conditions={"id": user_id})
    await db.dispose_instance()

# Run the script
asyncio.run(main())