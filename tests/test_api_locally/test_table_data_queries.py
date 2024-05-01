import unittest
from core.database.azure_sql import AzureSQLDatabase
from core.models.properties import PropertyOrm

class TestPaginateQuery(unittest.TestCase):
    def setUp(self):
        self.db = AzureSQLDatabase()
        self.model_class = PropertyOrm
        self.page_number = 0
        self.page_size = 10
        self.sort_by = 'created'
        self.sort_direction = 'asc'
        self.columns = ['id', 'street_name', 'city', 'price']
        self.conditions = {'type': 'residential'}

    def test_paginate_query(self):
        # Call the method
        result, total_items, total_pages = self.db.paginate_query(
            self.model_class, self.page_number, self.page_size, self.sort_by, self.sort_direction, self.columns, **self.conditions
        )

        # Assertions
        print(result)

if __name__ == '__main__':
    unittest.main()
