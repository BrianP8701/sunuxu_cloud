import asyncio
import os
from dotenv import load_dotenv

from core.database import Database
from core.models import *

# load_dotenv()
# db_url = os.getenv("AZURE_POSTGRES_CONN_STRING")
# print(db_url)

async def update_columns():
    db = Database()
    await db.delete_tables()
    await db.create_tables()
    tables = await db.list_tables()
    print(f"Created Tables:")
    print(tables)


asyncio.run(update_columns())
