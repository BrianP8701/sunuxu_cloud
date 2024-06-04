# api/base/update_transaction/main.py
import azure.functions as func

from core.database import Database
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route(
    route="update_transaction", methods=["PUT"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def update_transaction(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()

    data = req.get_json()

    transaction = DealOrm(
        id=data.get("id"),
        user_id=data.get("user_id"),
        property_id=data.get("property_id"),
        type=data.get("type"),
        status=data.get("status"),
        notes=data.get("notes"),
        description=data.get("description"),
    )

    await db.update(transaction)

    return func.HttpResponse(status_code=200, mimetype="application/json")
