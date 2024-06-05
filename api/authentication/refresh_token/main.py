# api/authentication/refresh_token/main.py
import json

import azure.functions as func

from api.api_utils import api_error_handler, return_server_error
from core.utils.security import refresh_access_token

blueprint = func.Blueprint()


@blueprint.route(
    route="refresh_token", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
def refresh_token(req: func.HttpRequest) -> func.HttpResponse:
    refresh_token = req.headers.get("Authorization", "").split(" ")[1]
    if not refresh_token:
        return_server_error("No refresh token provided.", status_code=401)

    try:
        access_token, new_refresh_token = refresh_access_token(refresh_token)
        return func.HttpResponse(
            body=json.dumps(
                {"access_token": access_token, "refresh_token": new_refresh_token}
            ),
            status_code=200,
            mimetype="application/json",
        )
    except ValueError as e:
        return_server_error(str(e), status_code=401)
