# api/admin/delete_user/main.py
import azure.functions as func

from api.api_utils import (api_error_handler, parse_request_body,
                           return_server_error)
from core.database import Database
from core.models import UserRowModel

blueprint = func.Blueprint()


@blueprint.route(
    route="sunuxu/admin/delete_user",
    methods=["DELETE"],
    auth_level=func.AuthLevel.FUNCTION,
)
@api_error_handler
async def delete_user(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()

    req_body = parse_request_body(req)

    email = req_body.get("email")

    if not await db.exists(UserRowModel, {"email": email}):
        return return_server_error("User not found.", status_code=404)

    user_orm = await db.query(UserRowModel, {"email": email})
    user = user_orm[0]
    await db.delete(UserRowModel, {"email": user.email})

    return func.HttpResponse(status_code=200)
