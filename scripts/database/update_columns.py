import asyncio

from core.database.azure_postgresql import AzurePostgreSQLDatabase
from core.models import *


async def update_columns():
    db = AzurePostgreSQLDatabase()
    await db.delete_tables()
    await db.create_tables()


asyncio.run(update_columns())
