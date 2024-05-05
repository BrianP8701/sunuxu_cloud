# api/base/get_transaction/main.py
import azure.functions as func
import json

from core.database import AzurePostgreSQLDatabase
from core.models import *
from api.api_utils import api_error_handler, return_server_error

blueprint = func.Blueprint()

@blueprint.route(route="get_transaction/{id}", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
async def get_transaction(req: func.HttpRequest) -> func.HttpResponse:
    db = AzurePostgreSQLDatabase()


    id = int(req.route_params.get("id"))
    data = await db.query(TransactionOrm, {"id": id})
    data = data[0]
    
    return func.HttpResponse(
        body=json.dumps({'data': data.to_dict()}),
        status_code=200,
        mimetype="application/json"
    )
