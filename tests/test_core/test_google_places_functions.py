import unittest
import requests
import uuid

from tests.utils.generate_url import get_function_url


class TestGooglePLacesFunctions(unittest.TestCase):
    def test_address_autocomplete(self):
        query = "6726 Sel"
        session_token = uuid.uuid4()
        print(get_function_url(f"address_autocomplete/{query}/{session_token}"))
        data = requests.get(
            get_function_url(f"address_autocomplete/{query}/{session_token}")
        ).json()
        print(data)

    def test_get_place_details(self):
        place_id = "Eik2NzI2IFNlbGJ5IFN0cmVldCwgU2FuIEZyYW5jaXNjbywgQ0EsIFVTQSIuKiwKFAoSCftKzXyqf4-AERmeffXTyylyEhQKEgkhAGkAbZqFgBH_rXbwZxNQSg"
        session_token = uuid.uuid4()

        data = requests.get(
            get_function_url(f"get_place_details/{place_id}/{session_token}")
        ).json()
        print(data)


if __name__ == "__main__":
    unittest.main()
