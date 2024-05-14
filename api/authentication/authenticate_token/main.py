# api/authentication/authenticate_token/main.py
import azure.functions as func
import json

from core.database import AzurePostgreSQLDatabase
from core.models import UserOrm
from core.security import validate_token
from api.api_utils import api_error_handler, return_server_error

blueprint = func.Blueprint()


@blueprint.route(
    route="authenticate_token", methods=["GET"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def authenticate_token(req: func.HttpRequest) -> func.HttpResponse:
    db = AzurePostgreSQLDatabase()

    access_token = req.headers.get("Authorization", "").split(" ")[1]
    if not access_token:
        return_server_error("No access token provided.", status_code=401)

    try:
        id = validate_token(access_token)
        user = await db.query(UserOrm, {"id": id})
        user = user[0]

        return func.HttpResponse(
            body=json.dumps({"user": user.to_dict()}),
            status_code=200,
            mimetype="application/json",
        )
    except ValueError as e:
        return_server_error(str(e), status_code=401)
