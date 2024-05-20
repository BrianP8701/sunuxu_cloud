
from core.database import Database
from typing import List, Dict, Any

def get_rows(user_id: int, table: str, page_size: int, page_index: int, sort_by: str, sort_direction: str, include_types: Dict[str, bool], include_statuses: Dict[str, bool]) -> List[dict]:
    """
    Get rows from a table based on the provided parameters

    :param user_id: The ID of the user making the request
    :param table: The table to fetch data from
    :param page_size: The number of rows to fetch
    :param page_index: The index of the page to fetch
    :param sort_by: The column to sort by
    :param sort_direction: The direction to sort by, either "ascending" or "descending"
    :param include_types: The types to include in the query
    :param include_statuses: The statuses to include in the query for transactions, or active/inactive for person and property tables
    """
    
    
    sort_ascending = None
    if sort_direction.lower() == "ascending":
        sort_ascending = True
    elif sort_direction.lower() == "descending":
        sort_ascending = False
    else:
        raise ValueError(f"Invalid sort direction provided: {sort_direction}")

    conditions = get_conditions(table, include_types, include_statuses, user_id)


def get_conditions(table: str, include_types: Dict[str, bool], include_statuses: Dict[str, bool], user_id: int) -> Dict[str, Any]:
    """
    Get the conditions to filter rows by based on the provided parameters

    :param table: The table to fetch data from
    :param include_types: The types to include in the query
    :param include_statuses: The statuses to include in the query for transactions, or active/inactive for person and property tables
    :param user_id: The ID of the user making the request
    """
    conditions = {"user_id": user_id}

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
            if table == "transactions":
                if status == "unknown" and include_statuses[status]:
                    include_statuses_list.append(None)
                elif include_statuses[status]:
                    include_statuses_list.append(status)
            else:
                if status == "active" and include_statuses[status]:
                    include_statuses_list.append(True)
                elif status == "inactive" and include_statuses[status]:
                    include_statuses_list.append(False)
        if table == "transactions":
            conditions["status"] = include_statuses_list
        else:
            conditions["active"] = include_statuses_list

    return conditions