# api/base/add_person/main.py
import azure.functions as func
import json

from core.database import Database
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route(
    route="add_person", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def add_person(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()

    data = req.get_json()
    first_name = data.get("first_name")
    middle_name = data.get("middle_name", "")
    last_name = data.get("last_name")
    full_name = f"{first_name} {middle_name} {last_name}".replace("  ", " ").strip()

    person = PersonOrm(
        user_id=data.get("user_id"),
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        notes=data.get("notes"),
        language=data.get("language"),
    )
    inserted_person = await db.create(person)
    person_row = PersonRowOrm(
        id=inserted_person.id,
        name=full_name,
        email=data.get("email"),
        phone=data.get("phone"),
        type=data.get("type"),
        active=False,
    )
    await db.create(person_row)

    return func.HttpResponse(
        body=json.dumps({"data": inserted_person.to_dict()}),
        status_code=200,
        mimetype="application/json",
    )
