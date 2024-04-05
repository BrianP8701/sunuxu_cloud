# api/authentication/login/main.py
import azure.functions as func
import json

from core.database import AzureSQLDatabase
from core.models import UserOrm
from core.security import check_password, generate_tokens

db = AzureSQLDatabase()
bp = func.Blueprint()

@bp.route(route="authentication/login", auth_level=func.AuthLevel.FUNCTION)
@bp.function_name(name="login")
def login(req: func.HttpRequest) -> func.HttpResponse:
    username = req.params.get('username')
    password = req.params.get('password')

    user_orm = db.query(UserOrm, {"username": username})
    if len(user_orm) == 0:
        return func.HttpResponse(
            "Invalid username.",
            status_code=401
        )
    user = user_orm[0]
    if not check_password(user.password, password):
        return func.HttpResponse(
            "Invalid password.",
            status_code=401
        )
    access_token, refresh_token = generate_tokens(user.id)
    return func.HttpResponse(
        json.dumps({'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()}),
        status_code=200,
        mimetype='application/json'
    )
