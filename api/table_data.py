from api.api_utils import parse_request_body, api_error_handler, return_server_error
import azure.functions as func
import json

from core.database import AzureSQLDatabase
from core.models import *

db = AzureSQLDatabase()
blueprint = func.Blueprint()


"""
    const response = await fetch(generateBackendUrl("get_table_data"), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            table: table,
            page_size: page_size,
            page_index: page_index,
            sort_by: sort_by,
            sort_direction: sort_direction,
            include_statuses: include_statuses, # Dict[str, bool]
            include_types: include_types # Dict[str, bool]
        })
    });
"""

@blueprint.route(route="get_table_data", methods=['POST'], auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
def get_table_data(req: func.HttpRequest) -> func.HttpResponse:
    try:
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
            columns = ['street_number', 'street_name', 'city', 'unit_number', 'state', 'zip_code', 'country', 'status', 'type', 'price']
            data = db.paginate_query(PropertyOrm, page_index, page_size, sort_by, sort_direction, columns=columns, **conditions)

        # Format the address and prepare the response data
        formatted_data = [{
            'address': f"{item.street_number} {item.unit_number} {item.street_name}, {item.city}, {item.state} {item.zip_code}, {item.country}",
            'status': item.status,
            'type': item.type,
            'price': item.price
        } for item in data]

        return func.HttpResponse(
            body=json.dumps({"message": "Data fetched successfully", "data": formatted_data}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return return_server_error(str(e))