# /api/crm/get_table_data/main.py
from api.api_utils import parse_request_body, api_error_handler, return_server_error
import azure.functions as func
import json
import logging
import traceback

from core.database import AzurePostgreSQLDatabase
from core.models import *

blueprint = func.Blueprint()

@blueprint.route(route="get_table_data", methods=['POST'], auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
async def get_table_data(req: func.HttpRequest) -> func.HttpResponse:
    try:
        db = AzurePostgreSQLDatabase()


        req_body = parse_request_body(req)

        table = req_body.get('table')
        page_size = int(req_body.get('page_size'))
        page_index = int(req_body.get('page_index'))
        sort_by = req_body.get('sort_by')
        sort_direction = req_body.get('sort_direction')
        include_types = req_body.get('include_types')
        include_statuses = req_body.get('include_statuses')

        conditions = {}
        if include_types:
            conditions['type'] = [type for type, include in include_types.items() if include]
        if include_statuses:
            conditions['status'] = [status for status, include in include_statuses.items() if include]

        if table == 'properties':
            columns = ['street_number', 'street_name', 'city', 'unit_number', 'state', 'zip_code', 'country', 'status', 'type', 'price', 'id']
            data, total_items, total_pages = await db.paginate_query(PropertyOrm, page_index, page_size, sort_by, sort_direction, columns=columns, **conditions)

            # Format the address and prepare the response data
            formatted_data = [{
                'id': item.id,
                'address': f"{item.street_number} {item.unit_number} {item.street_name}, {item.city}, {item.state} {item.zip_code}, {item.country}",
                'status': item.status,
                'type': item.type,
                'price': item.price
            } for item in data]
        elif table == 'people':
            columns = ['first_name', 'middle_name', 'last_name', 'email', 'phone', 'type', 'status', 'id']
            data, total_items, total_pages = await db.paginate_query(PersonOrm, page_index, page_size, sort_by, sort_direction, columns=columns, **conditions)
            
            formatted_data = [{
                'id': item.id,
                'name': f"{item.first_name} {item.middle_name + ' ' if item.middle_name else ''}{item.last_name}",
                'email': item.email,
                'phone': item.phone,
                'type': item.type,
                'status': item.status
            } for item in data]
        elif table == 'transactions':
            columns = ['property_id', 'status', 'type', 'id']
            # Ensure the property relationship is loaded, adjust according to your ORM setup
            data, total_items, total_pages = await db.paginate_query(
                TransactionOrm, page_index, page_size, sort_by, sort_direction,
                columns=columns, join=PropertyOrm, **conditions
            )

            formatted_data = [{
                'id': item.id,
                'property_id': item.property_id,
                'status': item.status,
                'type': item.type,
                'address': f"{item.property.street_number} {item.property.unit_number if item.property.unit_number else ''} {item.property.street_name}, {item.property.city}, {item.property.state} {item.property.zip_code}, {item.property.country}" if item.property else "No property attached",
                'price': item.property.price if item.property else "N/A"
            } for item in data]
        else:
            return func.HttpResponse(
                body=json.dumps({"message": "Invalid table name provided", "data": []}),
                status_code=400,
                mimetype="application/json"
            )

        return func.HttpResponse(
            body=json.dumps({"message": "Data fetched successfully", "data": formatted_data, "total_items": total_items, "total_pages": total_pages}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"\n\nError fetching table data: {str(e)} {traceback.print_exc()}\n\n")
        return return_server_error(str(e))
