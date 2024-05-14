# api/base/add_person/main.py
import azure.functions as func
import json

from core.database import AzurePostgreSQLDatabase
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route(
    route="add_person", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def add_person(req: func.HttpRequest) -> func.HttpResponse:
    db = AzurePostgreSQLDatabase()

    data = req.get_json()
    person = PersonOrm(
        user_id=data.get("user_id"),
        first_name=data.get("first_name"),
        middle_name=data.get("middle_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        phone=data.get("phone"),
        notes=data.get("notes"),
        type=data.get("type"),
        status=data.get("status"),
        language=data.get("language"),
    )

    inserted_person = await db.insert(person)

    return func.HttpResponse(
        body=json.dumps({"data": inserted_person.to_dict()}),
        status_code=200,
        mimetype="application/json",
    )
