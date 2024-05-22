import pytest
from core.database import Database
from core.models import *

@pytest.mark.database
@pytest.mark.asyncio
async def test_person_orm():
    db = Database()
    person = PersonDetailsOrm(
        user_id=1,
        first_name="John",
        middle_name="Doe",
        last_name="Smith",
        notes="This is a test note",
        language="english",
    )
    await db.insert(person)
    person = await db.get(PersonDetailsOrm, person.id)
    assert person.notes == "This is a test note"
    assert person.language == "english"
    person_row = PersonOrm(
        user_id=1,
        id=person.id,
        name="John Doe Smith",
        type="lead",
        active=True,
    )
    await db.insert(person_row)
    person_row = await db.get(PersonOrm, person_row.id)
    assert person_row.name == "John Doe Smith"
    assert person_row.type == "lead"
    assert person_row.active == True
    await db.delete(PersonDetailsOrm, {"id": person.id})
    # Ensure delete cascade works
    person_row_exists = await db.exists(PersonOrm, {"id": person.id})
    assert not person_row_exists

@pytest.mark.database
@pytest.mark.asyncio
async def test_property_orm():
    db = Database()
    # Create a new property
    new_property = PropertyDetailsOrm(
        user_id=1,
        street_number="123",
        street_name="Main",
        street_suffix="St",
        city="Anytown",
        state="CA",
        zip_code="90210",
        country="USA",
        notes="New property for testing",
        description="Detailed description here"
    )
    await db.insert(new_property)

    # Retrieve the property
    retrieved_property = await db.get(PropertyDetailsOrm, new_property.id)
    assert retrieved_property.street_name == "Main"
    assert retrieved_property.notes == "New property for testing"

    # Update the property
    retrieved_property.notes = "Updated note"
    await db.update(retrieved_property)

    updated_property = await db.get(PropertyDetailsOrm, new_property.id)
    assert updated_property.notes == "Updated note"

    # Delete the property
    await db.delete(PropertyDetailsOrm, {"id": new_property.id})

    deleted_property = await db.get(PropertyDetailsOrm, new_property.id)
    assert deleted_property is None

@pytest.mark.database
@pytest.mark.asyncio
async def test_transaction_orm():
    db = Database()
    # Create a new transaction
    new_transaction = DealDetailsOrm(
        user_id=1,
        property_id=1,
        notes="Initial transaction",
        description="Transaction description"
    )
    await db.insert(new_transaction)

    # Retrieve the transaction
    retrieved_transaction = await db.get(DealDetailsOrm, new_transaction.id)
    assert retrieved_transaction.notes == "Initial transaction"

    # Update the transaction
    retrieved_transaction.notes = "Updated transaction note"
    await db.update(retrieved_transaction)

    updated_transaction = await db.get(DealDetailsOrm, new_transaction.id)
    assert updated_transaction.notes == "Updated transaction note"

    # Delete the transaction
    await db.delete(DealDetailsOrm, {"id": new_transaction.id})

    deleted_transaction = await db.get(DealDetailsOrm, new_transaction.id)
    assert deleted_transaction is None
