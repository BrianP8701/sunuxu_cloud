import asyncio
import os

from dotenv import load_dotenv

from core.database import Database
from core.models import *

load_dotenv()
db_url = os.getenv("AZURE_POSTGRES_CONN_STRING")
print(db_url)

async def restart_database():
    """
    This function will delete all tables in the database and recreate them.
    """
    db = Database()
    await db.delete_tables()
    await db.create_tables()
    tables = await db.list_tables()
    print(f"Created Tables:")
    print(tables)

if __name__ == "__main__":
    asyncio.run(restart_database())
