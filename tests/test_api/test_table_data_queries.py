import unittest

import requests

from tests.utils.get_url import get_function_url


class TestTableDataRoutes(unittest.TestCase):
    def setUp(self):
        self.base_url = get_function_url("get_table_data")

    # # def test_properties_data(self):
    # #     data = {
    # #         "table": "properties",
    # #         "page_size": 10,
    # #         "page_index": 0,
    # #         "sort_by": "created",
    # #         "sort_direction": "new",
    # #         "include_types": {"residential": True, "commercial": True, "condo": False, "coop": True, "land": False, "hoa": False, "industrial": False, "rental": False, "other": False},
    # #         "include_statuses": {"active": True, "inactive": False}
    # #     }
    # #     response = requests.post(self.base_url, json=data)
    # #     self.assertEqual(response.status_code, 200)
    # #     print("Properties Data:", response.json())

    def test_people_data(self):
        data = {
            "table": "people",
            "page_size": 5,
            "page_index": 0,
            "sort_by": "created",
            "sort_direction": "new",
            "include_types": {
                "lead": True,
                "client": True,
                "prospect": True,
                "past_client": True,
                "agent": True,
                "broker": True,
                "attorney": True,
                "other": False,
                "unknown": True,
            },
            "include_statuses": {"active": True, "inactive": True, "unknown": True},
        }
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 200)
        print("People Data:", response.json())

    # def test_transactions_data(self):
    #     data = {
    #         "table": "transactions",
    #         "page_size": 5,
    #         "page_index": 0,
    #         "sort_by": "updated",
    #         "sort_direction": "new",
    #         "include_types": {"sale": True, "rent": False, "expired": False, "lease": False, "buy": False, "other": False},
    #         "include_statuses": {"pending": True, "closed": False, "expired": False, "withdrawn": False, "off_market": False, "other": False}
    #     }
    #     response = requests.post(self.base_url, json=data)
    #     self.assertEqual(response.status_code, 200)
    #     print("Transactions Data:", response.json())


if __name__ == "__main__":
    unittest.main()
