# api/authentication/signin/main.py
import json

import azure.functions as func

from api.api_utils import (api_error_handler, parse_request_body,
                           return_server_error)
from core.database import Database
from core.models import UserRowModel
from core.utils.security import check_password, generate_tokens

blueprint = func.Blueprint()


@blueprint.route(route="signin", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
async def signin(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()

    req_body = parse_request_body(req)

    if not await db.exists(UserRowModel, {"email": req_body["email"]}):
        return return_server_error(
            "An account with this email does not exist.", status_code=400
        )

    user = await db.query(UserRowModel, {"email": req_body["email"]})
    user = user[0]

    if not check_password(user.password, req_body["password"]):
        return return_server_error("Incorrect password.", status_code=400)

    access_token, refresh_token = generate_tokens(user.id)
    return func.HttpResponse(
        body=json.dumps(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.to_dict(),
            }
        ),
        status_code=200,
        mimetype="application/json",
    )
