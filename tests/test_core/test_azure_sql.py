import unittest
from dotenv import load_dotenv
import asyncio

from core.database.azure_postgresql import AzurePostgreSQLDatabase
from core.models.users import UserOrm

load_dotenv()

class AzureSQLDatabaseTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Ensure each test gets a fresh instance if needed.
        self.db = AzurePostgreSQLDatabase()
        print("Database instance created.")
    
    async def asyncTearDown(self):
        # Properly dispose of the instance after each test to prevent connection leaks.
        await AzurePostgreSQLDatabase.dispose_instance()

    async def test_insert_query_and_delete(self):
        # Create a user
        user = UserOrm(
            email="john@example.com",
            password="password",
            phone="1234567890",
            first_name="John",
            middle_name="",
            last_name="Doe"
        )
        inserted_user = await self.db.insert(user)

        # Query the user
        users = await self.db.query(UserOrm, {"email": "john@example.com"})
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, "john@example.com")
        
        # Delete the user
        await self.db.delete(UserOrm, {"id": inserted_user.id})

    async def test_update(self):
        # Create a user
        user = UserOrm(
            email="update@example.com",
            password="password",
            phone="1234567890",
            first_name="Update",
            middle_name="Middle",
            last_name="User"
        )
        inserted_user = await self.db.insert(user)

        # Update the user
        inserted_user.phone = "0987654321"
        await self.db.update(inserted_user)

        # Query the updated user
        users = await self.db.query(UserOrm, {"id": inserted_user.id})
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].phone, "0987654321")
        
        await self.db.delete(UserOrm, {"id": inserted_user.id})

    async def test_execute_raw_sql(self):
        # Create a user
        user = UserOrm(
            email="rawsql@example.com",
            password="password",
            phone="1234567890",
            first_name="RawSQL",
            middle_name="",
            last_name="User"
        )
        inserted_user = await self.db.insert(user)

        try:
            # Execute raw SQL query
            sql = "SELECT COUNT(*) FROM users WHERE email = 'rawsql@example.com'"
            result = await self.db.execute_raw_sql(sql)
            self.assertEqual(result[0][0], 1)
        finally:
            await self.db.delete(UserOrm, {"id": inserted_user.id})

    async def test_transactions(self):
        async def operations(session):
            user = UserOrm(
                email="transaction@example.com",
                password="password",
                phone="1111111111",
                first_name="Transaction",
                middle_name="",
                last_name="User"
            )
            session.add(user)

        try:
            # Perform the transaction
            await self.db.perform_transaction(operations)

            # Query the user after the transaction
            users = await self.db.query(UserOrm, {"email": "transaction@example.com"})
            self.assertEqual(len(users), 1)
        finally:
            await self.db.delete(UserOrm, {"email": "transaction@example.com"})


    async def test_exists(self):
        # Create a user
        user = UserOrm(
            email="exists@example.com",
            password="password",
            phone="1234567890",
            first_name="Exists",
            middle_name="",
            last_name="User"
        )

        try:
            # Insert the user
            inserted_user = await self.db.insert(user)

            # Check if the user exists
            exists = await self.db.exists(UserOrm, {"email": "exists@example.com"})
            self.assertTrue(exists)

            # Check if a non-existing user exists
            not_exists = await self.db.exists(UserOrm, {"email": "non_existing_user@example.com"})
            self.assertFalse(not_exists)
        finally:
            await self.db.delete(UserOrm, {"email": "exists@example.com"})


if __name__ == "__main__":
    unittest.main()