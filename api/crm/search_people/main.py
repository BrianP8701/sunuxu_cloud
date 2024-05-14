# /api/crm/search_people/main.py
from api.api_utils import api_error_handler, return_server_error
import azure.functions as func
import json
import logging
import traceback
from core.database import AzurePostgreSQLDatabase
from core.models import *

blueprint = func.Blueprint()

@blueprint.route(
    route="search_people", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def search_people(req: func.HttpRequest) -> func.HttpResponse:
    try:
        db = AzurePostgreSQLDatabase()
        
        req_body = req.get_json()
        user_id = req_body.get("user_id")
        search_term = req_body.get("search_term")
        search_type = req_body.get("search_type")

        if not search_type:
            if "@" in search_term and "." in search_term:
                search_type = 'email'
            elif search_term.isdigit():
                search_type = 'phone'
            else:
                search_type = 'name'
        
        conditions = {"user_id": user_id}
        
        if search_type == "name":
            conditions["name"] = search_term
        elif search_type == "email":
            conditions["email"] = search_term
        elif search_type == "phone":
            conditions["phone"] = search_term
        
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
        
        data = await db.similarity_search(
            PersonOrm, columns=columns, **conditions
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
        
        return func.HttpResponse(
            body=json.dumps(
                {
                    "message": "Search completed successfully",
                    "data": formatted_data,
                }
            ),
            status_code=200,
            mimetype="application/json",
        )
    except Exception as e:
        logging.error(
            f"\n\nError searching people: {str(e)} {traceback.print_exc()}\n\n"
        )
        return return_server_error(str(e))
