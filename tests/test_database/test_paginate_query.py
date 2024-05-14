import unittest
import asyncio

from core.database.azure_postgresql import AzurePostgreSQLDatabase
from core.models import PersonOrm

async def test_paginate_people():
    db = AzurePostgreSQLDatabase()
    page_size = 5
    page_index = 0
    sort_by = 'created'
    sort_ascending = False
    conditions = {
        'type': ['lead', 'client', 'prospect', 'past_client', 'agent', 'broker', 'attorney', 'other', None],
        'status': ['active', 'inactive', None]
    }
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

    data, total_items, total_pages = await db.paginate_query(
        PersonOrm,
        page_index,
        page_size,
        sort_by,
        sort_ascending,
        columns=columns,
        **conditions,
    )

    print(total_items, total_pages)
    
    for item in data:
        print(item.id, item.first_name, item.middle_name, item.last_name, item.email, item.phone, item.type, item.status)

if __name__ == "__main__":
    asyncio.run(test_paginate_people())