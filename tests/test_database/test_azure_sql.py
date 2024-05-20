import pytest
from dotenv import load_dotenv

from core.database import Database
from core.models.user import UserOrm

load_dotenv()

@pytest.fixture
async def db_instance():
    db = Database()
    print("Database instance created.")
    yield db
    await db.dispose_instance()

@pytest.fixture(autouse=True)
async def reset_db_sequence():
    db = Database()
    await db.execute_raw_sql("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users))")

@pytest.mark.database
@pytest.mark.asyncio
async def test_insert_query_and_delete():
    db = Database()
    user = UserOrm(
        email="john@example.com",
        password="password",
        phone="1234567890",
        first_name="John",
        middle_name="",
        last_name="Doe",
    )
    inserted_user = await db.insert(user)
    users = await db.query(UserOrm, {"email": "john@example.com"})
    assert len(users) == 1
    assert users[0].email == "john@example.com"
    await db.delete(UserOrm, {"id": inserted_user.id})

@pytest.mark.database
@pytest.mark.asyncio
async def test_update():
    db = Database()
    # Create a user
    user = UserOrm(
        email="update@example.com",
        password="password",
        phone="1234567890",
        first_name="Update",
        middle_name="Middle",
        last_name="User",
    )
    inserted_user = await db.insert(user)

    # Update the user
    inserted_user.phone = "0987654321"
    await db.update(inserted_user)

    # Query the updated user
    users = await db.query(UserOrm, {"id": inserted_user.id})
    assert len(users) == 1
    assert users[0].phone == "0987654321"

    await db.delete(UserOrm, {"id": inserted_user.id})

@pytest.mark.database
@pytest.mark.asyncio
async def test_execute_raw_sql():
    db = Database()
    # Create a user
    user = UserOrm(
        email="rawsql@example.com",
        password="password",
        phone="1234567890",
        first_name="RawSQL",
        middle_name="",
        last_name="User",
    )
    inserted_user = await db.insert(user)

    try:
        # Execute raw SQL query
        sql = "SELECT COUNT(*) FROM users WHERE email = 'rawsql@example.com'"
        result = await db.execute_raw_sql(sql)
        assert result[0][0] == 1
    finally:
        await db.delete(UserOrm, {"id": inserted_user.id})

@pytest.mark.database
@pytest.mark.asyncio
async def test_transactions():
    db = Database()
    async def operations(session):
        user = UserOrm(
            email="transaction@example.com",
            password="password",
            phone="1111111111",
            first_name="Transaction",
            middle_name="",
            last_name="User",
        )
        session.add(user)

    try:
        # Perform the transaction
        await db.perform_transaction(operations)

        # Query the user after the transaction
        users = await db.query(UserOrm, {"email": "transaction@example.com"})
        assert len(users) == 1
    finally:
        await db.delete(UserOrm, {"email": "transaction@example.com"})

@pytest.mark.database
@pytest.mark.asyncio
async def test_exists():
    db = Database()
    # Create a user
    user = UserOrm(
        email="exists@example.com",
        password="password",
        phone="1234567890",
        first_name="Exists",
        middle_name="",
        last_name="User",
    )

    try:
        # Insert the user
        inserted_user = await db.insert(user)

        # Check if the user exists
        exists = await db.exists(UserOrm, {"email": "exists@example.com"})
        assert exists

        # Check if a non-existing user exists
        not_exists = await db.exists(
            UserOrm, {"email": "non_existing_user@example.com"}
        )
        assert not not_exists
    finally:
        await db.delete(UserOrm, {"email": "exists@example.com"})
