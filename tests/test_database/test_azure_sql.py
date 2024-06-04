import pytest
from dotenv import load_dotenv

from core.database.azure_postgresql import AzurePostgreSQLDatabase
from core.models.rows.user import UserRowOrm

load_dotenv()

@pytest.fixture
async def db_instance():
    db = AzurePostgreSQLDatabase()
    print("Database instance created.")
    yield db
    await db.dispose_instance()

@pytest.fixture(autouse=True)
async def reset_db_sequence():
    db = AzurePostgreSQLDatabase()
    await db.execute_raw_sql("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users))")

@pytest.mark.database
@pytest.mark.asyncio
async def test_insert_query_and_delete(db_instance):
    user = UserRowOrm(
        email="john@example.com",
        password="password",
        phone="1234567890",
        first_name="John",
        middle_name="",
        last_name="Doe",
    )
    inserted_user = await db_instance.create(user)
    users = await db_instance.query(UserRowOrm, {"email": "john@example.com"})
    assert len(users) == 1
    assert users[0].email == "john@example.com"
    await db_instance.delete(UserRowOrm, {"id": inserted_user.id})

@pytest.mark.database
@pytest.mark.asyncio
async def test_update(db_instance):
    # Create a user
    user = UserRowOrm(
        email="update@example.com",
        password="password",
        phone="1234567890",
        first_name="Update",
        middle_name="Middle",
        last_name="User",
    )
    inserted_user = await db_instance.create(user)

    # Update the user
    inserted_user.phone = "0987654321"
    await db_instance.update(inserted_user)

    # Query the updated user
    users = await db_instance.query(UserRowOrm, {"id": inserted_user.id})
    assert len(users) == 1
    assert users[0].phone == "0987654321"

    await db_instance.delete(UserRowOrm, {"id": inserted_user.id})

@pytest.mark.database
@pytest.mark.asyncio
async def test_execute_raw_sql(db_instance):
    # Create a user
    user = UserRowOrm(
        email="rawsql@example.com",
        password="password",
        phone="1234567890",
        first_name="RawSQL",
        middle_name="",
        last_name="User",
    )
    inserted_user = await db_instance.create(user)

    try:
        # Execute raw SQL query
        sql = "SELECT COUNT(*) FROM users WHERE email = 'rawsql@example.com'"
        result = await db_instance.execute_raw_sql(sql)
        assert result[0][0] == 1
    finally:
        await db_instance.delete(UserRowOrm, {"id": inserted_user.id})

@pytest.mark.database
@pytest.mark.asyncio
async def test_transactions(db_instance):
    async def operations(session):
        user = UserRowOrm(
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
        await db_instance.perform_transaction(operations)

        # Query the user after the transaction
        users = await db_instance.query(UserRowOrm, {"email": "transaction@example.com"})
        assert len(users) == 1
    finally:
        await db_instance.delete(UserRowOrm, {"email": "transaction@example.com"})

@pytest.mark.database
@pytest.mark.asyncio
async def test_exists(db_instance):
    # Create a user
    user = UserRowOrm(
        email="exists@example.com",
        password="password",
        phone="1234567890",
        first_name="Exists",
        middle_name="",
        last_name="User",
    )

    try:
        # Insert the user
        await db_instance.create(user)

        # Check if the user exists
        exists = await db_instance.exists(UserRowOrm, {"email": "exists@example.com"})
        assert exists

        # Check if a non-existing user exists
        not_exists = await db_instance.exists(
            UserRowOrm, {"email": "non_existing_user@example.com"}
        )
        assert not not_exists
    finally:
        await db_instance.delete(UserRowOrm, {"email": "exists@example.com"})
