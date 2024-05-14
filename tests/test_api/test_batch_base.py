# test/test_api_locally/test_batch_base.py
import unittest
import requests
from dotenv import load_dotenv

from tests.utils import get_function_url
from core.database import AzurePostgreSQLDatabase
from core.models import *

load_dotenv()


class TestBaseRoutesBatch(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.person_ids = []
        cls.property_ids = []
        cls.transaction_ids = []

    async def asyncSetUp(self):
        # Ensure each test gets a fresh instance if needed.
        self.db = AzurePostgreSQLDatabase()

    async def asyncTearDown(self):
        # Properly dispose of the instance after each test to prevent connection leaks.
        await AzurePostgreSQLDatabase.dispose_instance()

    def test_1_add_persons(self):
        url = get_function_url("add_person")
        persons_data = [
            {
                "user_id": 1,
                "first_name": f"Test{i}",
                "last_name": f"Person{i}",
                "email": f"test.person{i}@example.com",
                "phone": f"123456789{i}",
                "description": f"Test Person Description {i}",
            }
            for i in range(3)
        ]
        responses = [requests.post(url, json=data) for data in persons_data]
        for response in responses:
            self.assertEqual(response.status_code, 200)
            TestBaseRoutesBatch.person_ids.append(response.json()["data"]["id"])

    def test_2_get_persons(self):
        url = get_function_url("get_person")
        for id in TestBaseRoutesBatch.person_ids:
            response = requests.post(url, json={"id": id})
            self.assertEqual(response.status_code, 200)

    async def test_3_delete_persons(self):
        url = get_function_url("delete_person")
        response = requests.post(url, json={"id": TestBaseRoutesBatch.person_ids})
        self.assertEqual(response.status_code, 200)
        for id in TestBaseRoutesBatch.person_ids:
            is_deleted = await self.db.exists(PersonOrm, {"id": id})
            self.assertFalse(is_deleted)

    def test_1_add_properties(self):
        url = get_function_url("add_property")
        properties_data = [
            {
                "user_id": 1,
                "street_number": "123",
                "street_name": f"Test{i}",
                "street_suffix": "St",
                "city": "Test City",
                "state": "TS",
                "zip_code": "12345",
                "country": "US",
                "type": "residential",
                "status": "active",
                "description": f"Test Property Description {i}",
            }
            for i in range(3)
        ]
        responses = [requests.post(url, json=data) for data in properties_data]
        for response in responses:
            self.assertEqual(response.status_code, 200)
            TestBaseRoutesBatch.property_ids.append(response.json()["data"]["id"])

    def test_2_get_properties(self):
        url = get_function_url("get_property")
        for id in TestBaseRoutesBatch.property_ids:
            response = requests.post(url, json={"id": id})
            self.assertEqual(response.status_code, 200)

    async def test_3_delete_properties(self):
        url = get_function_url("delete_property")
        response = requests.post(url, json={"id": TestBaseRoutesBatch.property_ids})
        self.assertEqual(response.status_code, 200)
        for id in TestBaseRoutesBatch.property_ids:
            is_deleted = await self.db.exists(PropertyOrm, {"id": id})
            self.assertFalse(is_deleted)

    def test_1_add_transactions(self):
        url = get_function_url("add_transaction")
        transactions_data = [
            {
                "user_id": 1,
                "status": "pending",
                "type": "sale",
                "notes": f"Test Transaction Notes {i}",
                "description": f"Test Transaction Description {i}",
            }
            for i in range(3)
        ]
        responses = [requests.post(url, json=data) for data in transactions_data]
        for response in responses:
            self.assertEqual(response.status_code, 200)
            TestBaseRoutesBatch.transaction_ids.append(response.json()["data"]["id"])

    def test_2_get_transactions(self):
        url = get_function_url("get_transaction")
        for id in TestBaseRoutesBatch.transaction_ids:
            response = requests.post(url, json={"id": id})
            self.assertEqual(response.status_code, 200)

    async def test_3_delete_transactions(self):
        url = get_function_url("delete_transaction")
        response = requests.post(url, json={"id": TestBaseRoutesBatch.transaction_ids})
        self.assertEqual(response.status_code, 200)
        for id in TestBaseRoutesBatch.transaction_ids:
            is_deleted = await self.db.exists(TransactionOrm, {"id": id})
            self.assertFalse(is_deleted)


if __name__ == "__main__":
    unittest.main()
