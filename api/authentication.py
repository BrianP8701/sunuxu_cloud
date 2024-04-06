# api/authentication.py
import azure.functions as func
import json

from sunuxu.database import AzureSQLDatabase
from sunuxu.models import UserOrm
from sunuxu.security import check_password, generate_tokens, hash_password

db = AzureSQLDatabase()
blueprint = func.Blueprint()

@blueprint.route(route="signup", auth_level=func.AuthLevel.FUNCTION)
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
        params = {'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()},
        status_code=200,
        )

@blueprint.route(route="login", auth_level=func.AuthLevel.FUNCTION)
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
        params={'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()},
        status_code=200,
    )
