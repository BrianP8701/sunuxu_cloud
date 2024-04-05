# api/authentication/signup/main.py
import azure.functions as func
import json

from core.database import AzureSQLDatabase
from core.models import UserOrm
from core.security import hash_password, generate_tokens

db = AzureSQLDatabase()
bp = func.Blueprint()

@bp.route(route="authentication/signup", auth_level=func.AuthLevel.FUNCTION)
@bp.function_name(name="signup")
def signup(req: func.HttpRequest) -> func.HttpResponse:
    username = req.params.get('username')
    password = req.params.get('password')
    email = req.params.get('email')
    phone = req.params.get('phone')
    first_name = req.params.get('first_name')
    middle_name = req.params.get('middle_name')
    last_name = req.params.get('last_name')
    user_type = req.params.get('user_type')

    if db.query(UserOrm, {"username": username}):
        return func.HttpResponse(
            "Username already exists.",
            status_code=400
        )

    user = UserOrm(
        username=username,
        password=hash_password(password),
        email=email,
        phone=phone,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        user_type=user_type

    )
    db.insert(user)
    access_token, refresh_token = generate_tokens(user.id)
    return func.HttpResponse(
        json.dumps({'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()}),
        status_code=200,
        mimetype='application/json'
    )
