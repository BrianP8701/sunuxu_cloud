import unittest
from io import BytesIO

import requests
from pandas import read_excel

from tests.utils.get_url import get_function_url


class TestDownloads(unittest.TestCase):
    def test_download_people(self):
        url = get_function_url("download_people")
        people_ids = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
        ]  # Example IDs, replace with actual IDs you want to test
        columns = ["id", "first_name", "last_name", "email", "phone", "type"]

        data = {"people_ids": people_ids, "columns": columns}

        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        # Save the Excel file locally for manual review
        with open("downloaded_people.xlsx", "wb") as f:
            f.write(response.content)

        # Load the Excel file to verify contents
        df = read_excel(BytesIO(response.content))

        # Check if the DataFrame contains the correct columns
        self.assertListEqual(list(df.columns), columns)

        # Check if the DataFrame contains the correct number of rows
        self.assertEqual(len(df), len(people_ids))


if __name__ == "__main__":
    unittest.main()
