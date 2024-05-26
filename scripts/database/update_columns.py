import asyncio

from core.database import Database
from core.models import *


async def update_columns():
    db = Database()
    await db.delete_tables()
    await db.create_tables()


asyncio.run(update_columns())
