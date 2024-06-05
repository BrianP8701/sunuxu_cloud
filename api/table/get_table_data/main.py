# /api/crm/get_table_data/main.py
import json
import logging
import traceback

import azure.functions as func

from api.api_utils import (api_error_handler, parse_request_body,
                           return_server_error)
from core.database import Database
from core.models import *
from core.queries.paginate_rows import paginate_rows

blueprint = func.Blueprint()


@blueprint.route(
    route="get_table_data", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def get_table_data(req: func.HttpRequest) -> func.HttpResponse:
    """
    This endpoint fetches data to fill a table in the CRM frontend.

    :param user_id: The ID of the user whose data is being fetched
    :param table: The name of the table [properties, people, transactions]
    :param page_size: The number of items to fetch per page
    :param page_index: The index of the page to fetch
    :param sort_by: The column to sort by
    :param sort_direction: The direction to sort by
    :param include_types: The types to include in the query
    :param include_statuses: The statuses to include in the query
    """
    try:
        Database()

        req_body = parse_request_body(req)

        user_id = req_body.get("user_id")
        table = req_body.get("table")
        page_size = int(req_body.get("page_size"))
        page_index = int(req_body.get("page_index"))
        sort_by = req_body.get("sort_by")
        sort_direction = req_body.get("sort_direction")
        include_types = req_body.get("include_types")
        include_statuses = req_body.get("include_statuses")

        sort_ascending = None
        if type(sort_direction) == str:
            if sort_direction.lower() == "new":
                sort_ascending = False
            elif sort_direction.lower() == "old":
                sort_ascending = True
            else:
                return return_server_error(
                    f"Invalid sort direction provided: {sort_direction}"
                )

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

        conditions["user_id"] = user_id

        if table == "properties":
            columns = [
                "street_number",
                "street_name",
                "city",
                "unit",
                "state",
                "zip_code",
                "country",
                "status",
                "type",
                "price",
                "id",
            ]
            data, total_items, total_pages = await paginate_rows(
                PropertyModel,
                page_index,
                page_size,
                sort_by,
                sort_ascending,
                columns=columns,
                **conditions,
            )

            # Format the address and prepare the response data
            formatted_data = [
                {
                    "id": item.id,
                    "address": f"{item.street_number} {item.unit} {item.street_name}, {item.city}, {item.state} {item.zip_code}, {item.country}",
                    "status": item.status,
                    "type": item.type,
                    "price": item.price,
                }
                for item in data
            ]
        elif table == "people":
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
            data, total_items, total_pages = await paginate_rows(
                PersonModel,
                page_index,
                page_size,
                sort_by,
                sort_ascending,
                columns=columns,
                **conditions,
            )

            formatted_data = [
                {
                    "id": item.id,
                    "name": f"{item.first_name} {item.middle_name + ' ' if item.middle_name else ''}{item.last_name}",
                    "email": item.email,
                    "phone": item.phone,
                    "type": item.type,
                    "status": item.status,
                }
                for item in data
            ]
        elif table == "transactions":
            columns = ["property_id", "status", "type", "id"]
            # Ensure the property relationship is loaded, adjust according to your ORM setup
            eagerloads = [
                {
                    "relationship": "property",
                    "columns": [
                        "street_name",
                        "street_number",
                        "street_suffix",
                        "unit",
                        "city",
                        "state",
                        "zip_code",
                        "country",
                        "price",
                    ],
                }
            ]

            data, total_items, total_pages = await paginate_rows(
                DealModel,
                page_index,
                page_size,
                sort_by,
                sort_ascending,
                columns=columns,
                eagerloads=eagerloads,
                **conditions,
            )

            # Use the eager-loaded data to format the response
            formatted_data = [
                {
                    "id": item.id,
                    "address": f"{item.property.street_number} {item.property.unit if item.property.unit else ''} {item.property.street_name}, {item.property.city}, {item.property.state} {item.property.zip_code}, {item.property.country}"
                    if item.property
                    else "No property attached",
                    "status": item.status,
                    "type": item.type,
                    "price": item.property.price if item.property else "N/A",
                }
                for item in data
            ]

        else:
            return func.HttpResponse(
                body=json.dumps({"message": "Invalid table name provided"}),
                status_code=400,
                mimetype="application/json",
            )

        return func.HttpResponse(
            body=json.dumps(
                {
                    "message": "Data fetched successfully",
                    "data": formatted_data,
                    "total_items": total_items,
                    "total_pages": total_pages,
                }
            ),
            status_code=200,
            mimetype="application/json",
        )
    except Exception as e:
        logging.error(
            f"\n\nError fetching table data: {str(e)} {traceback.print_exc()}\n\n"
        )
        return return_server_error(str(e))
