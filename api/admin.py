# api/admin.py
import azure.functions as func

from core.database import AzureSQLDatabase
from core.models import UserOrm

from api.api_utils import parse_request_body, api_error_handler, return_server_error

db = AzureSQLDatabase()
blueprint= func.Blueprint()


@blueprint.route(route="sunuxu/admin/delete_user", auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
def delete_user(req: func.HttpRequest) -> func.HttpResponse:
    """
    Called with email.
    """
    req_body = parse_request_body(req)

    email = req_body.get('email')

    if email:
        user_orm = db.query(UserOrm, {"email": email})
    else:
        return_server_error("User ID or email is required.", status_code=400)

    if len(user_orm) == 0:
        return_server_error("User not found.", status_code=404)

    user = user_orm[0]
    db.delete(UserOrm, {"email": user.email})

    return func.HttpResponse(
        status_code=200
    )
