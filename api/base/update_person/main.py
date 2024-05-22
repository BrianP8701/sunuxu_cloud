# api/base/update_person/main.py
import azure.functions as func

from core.database import Database
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route(
    route="update_person", methods=["PUT"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def update_person(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()

    data = req.get_json()

    person = PersonDetailsOrm(
        id=data.get("id"),
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
        created=data.get("created"),
        viewed=data.get("viewed"),
    )

    await db.update(person)

    return func.HttpResponse(status_code=200, mimetype="application/json")
