# api/admin.py
import azure.functions as func

from core.database import AzureSQLDatabase
from core.models import UserOrm
from core.utils.api_decorator import api_error_handler

db = AzureSQLDatabase()
blueprint= func.Blueprint()


@blueprint.route(route="admin/delete_user", auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
def delete_user(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.params.get('user_id')
    username = req.params.get('username')
    
    if user_id:
        user_orm = db.query(UserOrm, {"id": user_id})
    elif username:
        user_orm = db.query(UserOrm, {"username": username})
    else:
        return func.HttpResponse(
            "User ID or username is required.",
            status_code=400
        )

    if len(user_orm) == 0:
        return func.HttpResponse(
            "User not found.",
            status_code=404
        )

    user = user_orm[0]
    db.delete(user)

    return func.HttpResponse(
        status_code=200
    )
