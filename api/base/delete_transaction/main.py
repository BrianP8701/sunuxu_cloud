# api/base/delete_transaction/main.py
import azure.functions as func

from api.api_utils import api_error_handler
from core.database import Database
from core.models import *

blueprint = func.Blueprint()


@blueprint.route(
    route="delete_transaction", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def delete_transaction(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()
    data = req.get_json()["id"]

    if isinstance(data, list):
        await db.batch_delete(DealModel, {"id": data})
    else:
        await db.delete(DealModel, {"id": data})

    return func.HttpResponse(status_code=200, mimetype="application/json")
