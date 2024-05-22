# api/base/get_person/main.py
import azure.functions as func
import json

from core.database import Database
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route(
    route="get_person", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def get_person(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()
    data = req.get_json()["id"]

    if isinstance(data, list):
        results = await db.batch_query(PersonDetailsOrm, {"id": data})
    else:
        results = await db.query(PersonDetailsOrm, {"id": data})

    if not results:
        return func.HttpResponse(
            body=json.dumps({"message": "Person not found"}),
            status_code=404,
            mimetype="application/json",
        )

    return func.HttpResponse(
        body=json.dumps({"data": [result.to_dict() for result in results]}),
        status_code=200,
        mimetype="application/json",
    )
