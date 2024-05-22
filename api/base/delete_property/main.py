# api/base/delete_property/main.py
import azure.functions as func
import json

from core.database import Database
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route(
    route="delete_property", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def delete_property(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()
    data = req.get_json()["id"]

    if isinstance(data, list):
        await db.batch_delete(PropertyDetailsOrm, {"id": data})
    else:
        await db.delete(PropertyDetailsOrm, {"id": data})

    return func.HttpResponse(status_code=200, mimetype="application/json")
