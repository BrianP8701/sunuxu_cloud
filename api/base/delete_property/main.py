# api/base/delete_property/main.py
import azure.functions as func

from core.database import AzurePostgreSQLDatabase
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()

@blueprint.route(route="delete_property/{id}", methods=["DELETE"], auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
async def delete_property(req: func.HttpRequest) -> func.HttpResponse:
    db = AzurePostgreSQLDatabase()

    id = int(req.route_params.get("id"))

    await db.delete(PropertyOrm, {"id": id})

    return func.HttpResponse(
        status_code=200,
        mimetype="application/json"
   )
