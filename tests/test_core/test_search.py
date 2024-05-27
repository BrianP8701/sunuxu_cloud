# tests/test_core/test_search.py
import pytest
from core.database import Databasefrom core.models import *
from core.utils.search import search
from core.utils.security import hash_password
import faker

fake = faker.Faker()
user_id = 2

@pytest.fixture(scope="module")
async def setup_database():
    db = Database()
    yield
    await db.delete(UserOrm, conditions={"id": user_id})
    await db.dispose_instance()

@pytest.fixture(scope="module")
async def insert_test_data():
    db = Database()
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

    return user_id

@pytest.mark.core
@pytest.mark.asyncio
async def test_people_search_by_name(insert_test_data):
    user_id = insert_test_data
    results = await search("people", "UniqueFirstName", user_id)
    assert len(results) == 1
    assert results[0].name == "UniqueFirstName UniqueMiddleName UniqueLastName"

@pytest.mark.core
@pytest.mark.asyncio
async def test_people_search_by_name_typo(insert_test_data):
    user_id = insert_test_data
    results = await search("people", "UnikueFirstName UniqueMiddleName UniqueLastName", user_id)
    assert len(results) == 1
    assert results[0].name == "UniqueFirstName UniqueMiddleName UniqueLastName"

@pytest.mark.core
@pytest.mark.asyncio
async def test_property_search_by_address(insert_test_data):
    user_id = insert_test_data
    results = await search("properties", "123 UniqueStreet Ave", user_id)
    assert len(results) == 1
    assert results[0].address == "123 UniqueStreet Ave, UniqueCity, UniqueState, 12345"

@pytest.mark.core
@pytest.mark.asyncio
async def test_property_search_by_mls_number(insert_test_data):
    user_id = insert_test_data
    results = await search("properties", "12345678", user_id)
    assert len(results) == 1
    assert results[0].mls_number == "12345678"

@pytest.mark.core
@pytest.mark.asyncio
async def test_transaction_search_by_name(insert_test_data):
    user_id = insert_test_data
    results = await search("transactions", "UniqueTransactionName", user_id)
    assert len(results) == 1
    assert results[0].name == "UniqueTransactionName"

@pytest.mark.core
@pytest.mark.asyncio
async def test_transaction_search_by_name_typo(insert_test_data):
    user_id = insert_test_data
    results = await search("transactions", "UniqueTransactinName", user_id)
    assert len(results) == 1
    assert results[0].name == "UniqueTransactionName"
