# api/base/delete_person/main.py
import azure.functions as func

from core.database import Database
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route(
    route="delete_person", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def delete_person(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()
    data = req.get_json()["id"]

    if isinstance(data, list):
        await db.batch_delete(PersonDetailsOrm, {"id": data})
    else:
        await db.delete(PersonDetailsOrm, {"id": data})

    return func.HttpResponse(status_code=200, mimetype="application/json")
