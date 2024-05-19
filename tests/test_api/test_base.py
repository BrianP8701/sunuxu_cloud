# test/test_api_locally/test_base.py
import unittest
import requests
from dotenv import load_dotenv

from tests.utils.generate_url import get_function_url
from core.database import AzurePostgreSQLDatabase
from core.models import *

load_dotenv()


class TestBaseRoutes(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.person_id = None
        cls.property_id = None
        cls.transaction_id = None

    async def asyncSetUp(self):
        # Ensure each test gets a fresh instance if needed.
        self.db = AzurePostgreSQLDatabase()

    async def asyncTearDown(self):
        # Properly dispose of the instance after each test to prevent connection leaks.
        await AzurePostgreSQLDatabase.dispose_instance()

    def test_1_add_person(self):
        url = get_function_url("add_person")
        data = {
            "user_id": 1,
            "first_name": "Test",
            "last_name": "Person",
            "email": "test.person@example.com",
            "phone": "1234567890",
            "description": "Test Person Description",
        }
        response = requests.post(url, json=data)
        print("Add Person Response:\n", response.json())
        self.assertEqual(response.status_code, 200)
        TestBaseRoutes.person_id = response.json()["data"]["id"]

    def test_2_get_person(self):
        url = get_function_url("get_person")
        id = TestBaseRoutes.person_id
        response = requests.post(url, json={"id": id})
        print("Get Person Response:\n", response.json())
        self.assertEqual(response.status_code, 200)

    async def test_3_update_person(self):
        url = get_function_url("update_person")
        id = TestBaseRoutes.person_id
        data = {
            "user_id": 1,
            "id": id,
            "first_name": "Updated",
            "last_name": "Person",
            "email": "updated.person@example.com",
            "phone": "1234567890",
        }
        response = requests.put(url, json=data)
        self.assertEqual(response.status_code, 200)

        updated_person = await self.db.query(PersonOrm, {"id": id})
        updated_person = updated_person[0]
        self.assertEqual(updated_person.first_name, "Updated")
        self.assertEqual(updated_person.last_name, "Person")
        self.assertEqual(updated_person.email, "updated.person@example.com")
        self.assertEqual(updated_person.phone, "1234567890")

    async def test_4_delete_person(self):
        url = get_function_url("delete_person")
        id = TestBaseRoutes.person_id
        response = requests.post(url, json={"id": id})
        self.assertEqual(response.status_code, 200)
        is_deleted = await self.db.exists(PersonOrm, {"id": id})
        self.assertFalse(is_deleted)

    def test_1_add_property(self):
        url = get_function_url("add_property")
        data = {
            "user_id": 1,
            "street_number": "123",
            "street_name": "Test",
            "street_suffix": "St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
            "country": "US",
            "type": "residential",
            "status": "active",
            "description": "Test Property Description",
        }
        response = requests.post(url, json=data)
        print("Add Property Response:\n", response.json())
        self.assertEqual(response.status_code, 200)
        TestBaseRoutes.property_id = response.json()["data"]["id"]

    def test_2_get_property(self):
        url = get_function_url("get_property")
        id = TestBaseRoutes.property_id
        response = requests.post(url, json={"id": id})
        print("Get Property Response:\n", response.json())
        self.assertEqual(response.status_code, 200)

    async def test_3_update_property(self):
        url = get_function_url("update_property")
        id = TestBaseRoutes.property_id
        data = {
            "user_id": 1,
            "id": id,
            "street_number": "123",
            "street_name": "Updated",
            "street_suffix": "St",
            "city": "Updated City",
            "state": "TS",
            "zip_code": "12345",
            "country": "US",
            "type": "residential",
            "status": "active",
            "description": "Updated Property Description",
        }
        response = requests.put(url, json=data)

        self.assertEqual(response.status_code, 200)
        updated_property = await self.db.query(PropertyOrm, {"id": id})
        updated_property = updated_property[0]
        self.assertEqual(updated_property.street_name, "Updated")
        self.assertEqual(updated_property.city, "Updated City")
        self.assertEqual(updated_property.description, "Updated Property Description")
        self.assertEqual(updated_property.status, "active")
        self.assertEqual(updated_property.type, "residential")

    async def test_4_delete_property(self):
        url = get_function_url("delete_property")
        id = TestBaseRoutes.property_id
        response = requests.post(url, json={"id": id})
        self.assertEqual(response.status_code, 200)
        is_deleted = await self.db.exists(PropertyOrm, {"id": id})
        self.assertFalse(is_deleted)

    def test_1_add_transaction(self):
        url = get_function_url("add_transaction")
        data = {
            "user_id": 1,
            "status": "pending",
            "type": "sale",
            "notes": "Test Transaction Notes",
            "description": "Test Transaction Description",
        }
        response = requests.post(url, json=data)
        print("Add Transaction Response:\n", response.json())
        self.assertEqual(response.status_code, 200)
        TestBaseRoutes.transaction_id = response.json()["data"]["id"]

    def test_2_get_transaction(self):
        url = get_function_url("get_transaction")
        id = TestBaseRoutes.transaction_id
        response = requests.post(url, json={"id": id})
        print("Get Transaction Response:\n", response.json())
        self.assertEqual(response.status_code, 200)

    async def test_3_update_transaction(self):
        url = get_function_url("update_transaction")
        id = TestBaseRoutes.transaction_id
        data = {
            "user_id": 1,
            "id": id,
            "status": "closed",
            "type": "rent",
            "notes": "Updated Transaction Notes",
            "description": "Updated Transaction Description",
        }
        response = requests.put(url, json=data)
        self.assertEqual(response.status_code, 200)
        updated_transaction = await self.db.query(TransactionOrm, {"id": id})
        updated_transaction = updated_transaction[0]
        self.assertEqual(updated_transaction.status, "closed")
        self.assertEqual(updated_transaction.type, "rent")
        self.assertEqual(updated_transaction.notes, "Updated Transaction Notes")
        self.assertEqual(
            updated_transaction.description, "Updated Transaction Description"
        )

    async def test_4_delete_transaction(self):
        url = get_function_url("delete_transaction")
        id = TestBaseRoutes.transaction_id
        response = requests.post(url, json={"id": id})
        self.assertEqual(response.status_code, 200)
        is_deleted = await self.db.exists(TransactionOrm, {"id": id})
        self.assertFalse(is_deleted)


if __name__ == "__main__":
    unittest.main()
