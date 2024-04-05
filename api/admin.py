# api/admin.py
import azure.functions as func

from sunuxu.database import AzureSQLDatabase
from sunuxu.models import UserOrm

db = AzureSQLDatabase()
bp = func.Blueprint()


@bp.route(route="sunuxu/admin/delete_user", auth_level=func.AuthLevel.FUNCTION)
@bp.function_name(name="delete_user")
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
        "User deleted successfully.",
        status_code=200
    )
