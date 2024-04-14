# api/authentication.py
import azure.functions as func
import json

from core.database import AzureSQLDatabase
from core.models import UserOrm
from core.security import check_password, generate_tokens, hash_password
from api.api_utils import parse_request_body, api_error_handler, return_server_error

db = AzureSQLDatabase()
blueprint = func.Blueprint()

@blueprint.route(route="authentication/signup", auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
def signup(req: func.HttpRequest) -> func.HttpResponse:
    req_body = parse_request_body(req)

    if db.exists(UserOrm, {"email": req_body['email']}):
        return_server_error("Email already exists.", status_code=400)

    user = UserOrm(
        email=req_body['email'],
        password=hash_password(req_body['password']),
        phone=req_body['phone'],
        first_name=req_body['first_name'],
        middle_name=req_body['middle_name'],
        last_name=req_body['last_name'],
        user_type=req_body['user_type']
    )

    db.insert(user)
    access_token, refresh_token = generate_tokens(user.user_id)
    return func.HttpResponse(
        body=json.dumps({'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()}),
        status_code=200,
        mimetype="application/json"
    )

@blueprint.route(route="authentication/signin", auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
def signin(req: func.HttpRequest) -> func.HttpResponse:
    req_body = parse_request_body(req)

    if not db.exists(UserOrm, {"email": req_body['email']}):
        return_server_error("An account with this email does not exist.", status_code=400)

    user = db.query(UserOrm, {"email": req_body['email']})[0]

    if not check_password(user.password, req_body['password']):
        return_server_error("Incorrect password.", status_code=400)

    access_token, refresh_token = generate_tokens(user.user_id)
    return func.HttpResponse(
        body=json.dumps({'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()}),
        status_code=200,
        mimetype="application/json"
    )
