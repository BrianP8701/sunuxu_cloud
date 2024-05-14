# api/base/add_transaction/main.py
import azure.functions as func
import json

from core.database import AzurePostgreSQLDatabase
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route(
    route="add_transaction", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def add_transaction(req: func.HttpRequest) -> func.HttpResponse:
    db = AzurePostgreSQLDatabase()

    data = req.get_json()
    transaction = TransactionOrm(
        user_id=data.get("user_id"),
        property_id=data.get("property_id"),
        type=data.get("type"),
        status=data.get("status"),
        notes=data.get("notes"),
        description=data.get("description"),
    )

    inserted_transaction = await db.insert(transaction)

    return func.HttpResponse(
        body=json.dumps({"data": inserted_transaction.to_dict()}),
        status_code=200,
        mimetype="application/json",
    )
