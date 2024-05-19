import pytest

from core.database.azure_postgresql import AzurePostgreSQLDatabase
from core.models import *
from core.utils.paginate_rows import paginate_rows


@pytest.mark.database
@pytest.mark.asyncio
async def test_paginate_properties():
    include_types = {
        "unknown": True, 
        "condo": True, 
        "coop": True, 
        "residential": True,
        "commercial": True,
        "land": True,
        "hoa": True,
        "industrial": True,
        "rental": True,
        "other": True
    }
    include_statuses = {
        "active": True,
        "inactive": False
    }

    conditions = {}
    if include_types:
        include_types_list = []
        for type_ in include_types:
            if type_ == "unknown" and include_types[type_]:
                include_types_list.append(None)
            elif include_types[type_]:
                include_types_list.append(type_)
        conditions["type"] = include_types_list

    if include_statuses:
        include_statuses_list = []
        for status in include_statuses:
            if status == "active" and include_statuses[status]:
                include_statuses_list.append(True)
            elif status == "inactive" and include_statuses[status]:
                include_statuses_list.append(False)
        conditions["active"] = include_statuses_list     

    conditions["user_id"] = 1 

    properties, total_items, total_pages = await paginate_rows(
        PropertyRowOrm,
        page_number=0,
        page_size=10,
        sort_by="created",
        sort_ascending=True,
        **conditions
    )

    assert properties is not None
    assert len(properties) <= 10
    assert total_items is not None
    assert total_pages is not None
    
@pytest.mark.database
@pytest.mark.asyncio
async def test_paginate_people():
    include_types = {
        "unknown": True, 
        "client": True, 
        "agent": True,
        "other": True
    }
    include_statuses = {
        "active": True,
        "inactive": False
    }

    conditions = {}
    if include_types:
        include_types_list = []
        for type_ in include_types:
            if type_ == "unknown" and include_types[type_]:
                include_types_list.append(None)
            elif include_types[type_]:
                include_types_list.append(type_)
        conditions["type"] = include_types_list

    if include_statuses:
        include_statuses_list = []
        for status in include_statuses:
            if status == "active" and include_statuses[status]:
                include_statuses_list.append(True)
            elif status == "inactive" and include_statuses[status]:
                include_statuses_list.append(False)
        conditions["active"] = include_statuses_list

    conditions["user_id"] = 1 

    people, total_items, total_pages = await paginate_rows(
        PersonRowOrm,
        page_number=0,
        page_size=10,
        sort_by="created",
        sort_ascending=True,
        **conditions
    )

    assert people is not None
    assert len(people) <= 10
    assert total_items is not None
    assert total_pages is not None

@pytest.mark.database
@pytest.mark.asyncio
async def test_paginate_transactions():
    include_types = {
        "sell": True, 
        "buy": True, 
        "dual": False,
    }
    include_statuses = {
        "pending": True,
        "closed": False,
        "withdrawn": True,
        "off_market": True,
        "unknown": True
    }

    conditions = {}
    if include_types:
        include_types_list = []
        for type_ in include_types:
            if type_ == "unknown" and include_types[type_]:
                include_types_list.append(None)
            elif include_types[type_]:
                include_types_list.append(type_)
        conditions["type"] = include_types_list

    if include_statuses:
        include_statuses_list = []
        for status in include_statuses:
            if status == "unknown" and include_statuses[status]:
                include_statuses_list.append(None)
            elif include_statuses[status]:
                include_statuses_list.append(status)
        conditions["status"] = include_statuses_list

    conditions["user_id"] = 1  # Example user_id

    transactions, total_items, total_pages = await paginate_rows(
        TransactionRowOrm,
        page_number=0,
        page_size=10,
        sort_by="created",
        sort_ascending=True,
        **conditions
    )

    assert transactions is not None
    assert len(transactions) <= 10
    assert total_items is not None
    assert total_pages is not None
