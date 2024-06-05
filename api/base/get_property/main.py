# api/base/get_property/main.py
import json

import azure.functions as func

from api.api_utils import api_error_handler
from core.database import Database
from core.models import *

blueprint = func.Blueprint()


@blueprint.route(
    route="get_property", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def get_property(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()
    data = req.get_json()["id"]

    if isinstance(data, list):
        results = await db.batch_query(PropertyModel, {"id": data})
    else:
        results = await db.query(PropertyModel, {"id": data})

    return func.HttpResponse(
        body=json.dumps({"data": [result.to_dict() for result in results]}),
        status_code=200,
        mimetype="application/json",
    )
