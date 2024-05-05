# api/base/delete_person/main.py
import azure.functions as func
import json

from core.database import AzurePostgreSQLDatabase
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()

@blueprint.route(route="delete_person", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
async def delete_person(req: func.HttpRequest) -> func.HttpResponse:
    db = AzurePostgreSQLDatabase()
    data = req.get_json()["id"]

    if isinstance(data, list):
        await db.batch_delete(PersonOrm, {"id": data})
    else:
        await db.delete(PersonOrm, {"id": data})

    return func.HttpResponse(
        status_code=200,
        mimetype="application/json"
    )