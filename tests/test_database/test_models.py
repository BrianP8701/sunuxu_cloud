import pytest
from core.database import Database
from core.models import *

@pytest.mark.database
@pytest.mark.asyncio
async def test_person_orm():
    db = Database()
    person = PersonOrm(
        user_id=1,
        first_name="John",
        middle_name="Doe",
        last_name="Smith",
        notes="This is a test note",
        language="english",
    )
    await db.create(person)
    person = await db.read(PersonOrm, person.id)
    assert person.notes == "This is a test note"
    assert person.language == "english"
    person_row = PersonRowOrm(
        user_id=1,
        id=person.id,
        name="John Doe Smith",
        type="lead",
        active=True,
    )
    await db.create(person_row)
    person_row = await db.read(PersonRowOrm, person_row.id)
    assert person_row.name == "John Doe Smith"
    assert person_row.type == "lead"
    assert person_row.active is True
    await db.delete(PersonOrm, {"id": person.id})
    # Ensure delete cascade works
    person_row_exists = await db.exists(PersonRowOrm, {"id": person.id})
    assert not person_row_exists

@pytest.mark.database
@pytest.mark.asyncio
async def test_property_orm():
    db = Database()
    # Create a new property
    new_property = PropertyOrm(
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
    await db.create(new_property)

    # Retrieve the property
    retrieved_property = await db.read(PropertyOrm, new_property.id)
    assert retrieved_property.street_name == "Main"
    assert retrieved_property.notes == "New property for testing"

    # Update the property
    retrieved_property.notes = "Updated note"
    await db.update(retrieved_property)

    updated_property = await db.read(PropertyOrm, new_property.id)
    assert updated_property.notes == "Updated note"

    # Delete the property
    await db.delete(PropertyOrm, {"id": new_property.id})

    deleted_property = await db.read(PropertyOrm, new_property.id)
    assert deleted_property is None

@pytest.mark.database
@pytest.mark.asyncio
async def test_transaction_orm():
    db = Database()
    # Create a new transaction
    new_transaction = DealOrm(
        user_id=1,
        property_id=1,
        notes="Initial transaction",
        description="Transaction description"
    )
    await db.create(new_transaction)

    # Retrieve the transaction
    retrieved_transaction = await db.read(DealOrm, new_transaction.id)
    assert retrieved_transaction.notes == "Initial transaction"

    # Update the transaction
    retrieved_transaction.notes = "Updated transaction note"
    await db.update(retrieved_transaction)

    updated_transaction = await db.read(DealOrm, new_transaction.id)
    assert updated_transaction.notes == "Updated transaction note"

    # Delete the transaction
    await db.delete(DealOrm, {"id": new_transaction.id})

    deleted_transaction = await db.read(DealOrm, new_transaction.id)
    assert deleted_transaction is None
