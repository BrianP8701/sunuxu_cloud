import unittest
from dotenv import load_dotenv
import asyncio

from core.database.azure_postgresql import AzurePostgreSQLDatabase
from core.models import *

load_dotenv()


# class AzureSQLDatabaseTestCase(unittest.IsolatedAsyncioTestCase):
#     async def asyncSetUp(self):
#         # Ensure each test gets a fresh instance if needed.
#         self.db = AzurePostgreSQLDatabase()
#         print("Database instance created.")

#     async def asyncTearDown(self):
#         # Properly dispose of the instance after each test to prevent connection leaks.
#         await AzurePostgreSQLDatabase.dispose_instance()

#     async def search_people(self):
#         search = "Rick"
#         conditions = {"name": search}
#         columns = [
#             "first_name",
#             "middle_name",
#             "last_name",
#             "email",
#             "phone",
#             "type",
#             "status",
#             "id",
#         ]
#         response = await self.db.similarity_search(PersonOrm, columns, conditions)

#         print(response)

# if __name__ == "__main__":
#     unittest.main()


async def search_people():
    db = AzurePostgreSQLDatabase()
    search = "Rick przezdziecki"
    conditions = {"name": search}
    columns = [
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "phone",
        "type",
        "status",
        "id",
    ]
    response = await db.similarity_search(PersonOrm, columns, **conditions)

    for thing in response:
        formatted_data = {
            "id": thing.id,
            "name": f"{thing.first_name} {thing.middle_name + ' ' if thing.middle_name else ''}{thing.last_name}",
            "email": thing.email,
            "phone": thing.phone,
            "type": thing.type,
            "status": thing.status,
        }
        print(formatted_data)


asyncio.run(search_people())
