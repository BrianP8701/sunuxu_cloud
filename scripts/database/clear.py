import asyncio
import os

from dotenv import load_dotenv

from core.database.azure_postgresql import AzurePostgreSQLDatabase
from core.models import *

load_dotenv()
db_url = os.getenv("AZURE_POSTGRES_CONN_STRING")
print(db_url)

async def clear_database():
    """
    This function will clear all tables in the database.
    """
    db = AzurePostgreSQLDatabase()
    await db.clear_tables()
    tables = await db.list_tables()
    print(f"Cleared Tables:")
    print(tables)

if __name__ == "__main__":
    asyncio.run(clear_database())
