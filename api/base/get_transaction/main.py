# api/base/get_transaction/main.py
import json

import azure.functions as func

from api.api_utils import api_error_handler
from core.database import Database
from core.models import *

blueprint = func.Blueprint()


@blueprint.route(
    route="get_transaction", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def get_transaction(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()
    data = req.get_json()["id"]

    if isinstance(data, list):
        results = await db.batch_query(DealModel, {"id": data})
    else:
        results = await db.query(DealModel, {"id": data})

    return func.HttpResponse(
        body=json.dumps({"data": [result.to_dict() for result in results]}),
        status_code=200,
        mimetype="application/json",
    )
