# conftest.py
import pytest
import logging

from core.database.azure_postgresql import AzurePostgreSQLDatabase
from tests.utils.generate_fake_data import generate_fake_data

# # Configure logging to write to a local file called logs.txt with 2 new lines in between each log
# logging.basicConfig(
#     filename='logs.txt',
#     filemode='a',
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s\n\n',
#     level=logging.INFO
# )


@pytest.fixture(scope="session", autouse=True)
async def global_setup():
    """
    Clear and update database tables and generate fake data before running tests
    """
    db = AzurePostgreSQLDatabase()
    await db.delete_tables()
    await db.create_tables()
    await generate_fake_data()
    yield
    await db.clear_tables()



# @pytest.fixture(scope="module", autouse=True)
# def database_setup(pytestconfig):
#     if pytestconfig.getoption("-m") == "database":
#         print("Setup for database tests")
#         # Setup code here
#         yield
#         print("Teardown for database tests")
#         # Teardown code here

# @pytest.fixture(scope="module", autouse=True)
# def logic_setup():
#     print("Setup for logic tests")
#     yield
#     print("Teardown for logic tests")

# @pytest.fixture(scope="module", autouse=True)
# def azure_function_setup():
#     print("Setup for Azure function tests")
#     yield
#     print("Teardown for Azure function tests")
