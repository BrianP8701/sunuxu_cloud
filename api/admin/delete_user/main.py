# api/admin/delete_user/main.py
import azure.functions as func

from core.database import Database
from core.models import UserOrm

from api.api_utils import parse_request_body, api_error_handler, return_server_error

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

    if not await db.exists(UserOrm, {"email": email}):
        return return_server_error("User not found.", status_code=404)

    user_orm = await db.query(UserOrm, {"email": email})
    user = user_orm[0]
    await db.delete(UserOrm, {"email": user.email})

    return func.HttpResponse(status_code=200)
