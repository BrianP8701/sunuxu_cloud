# api/base/get_person/main.py
import azure.functions as func
import json

from core.database import AzurePostgreSQLDatabase
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()

@blueprint.route(route="get_person/{id}", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
async def get_person(req: func.HttpRequest) -> func.HttpResponse:
    db = AzurePostgreSQLDatabase()

    id = int(req.route_params.get("id"))

    data = await db.query(PersonOrm, {"id": id})
    if not data:
        return func.HttpResponse(
            body=json.dumps({'message': 'Person not found'}),
            status_code=404,
            mimetype="application/json"
        )
    data = data[0]

    return func.HttpResponse(
        body=json.dumps({'data': data.to_dict()}),
        status_code=200,
        mimetype="application/json"
    )
