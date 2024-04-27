# api/authentication.py
import azure.functions as func
import json

from core.database import AzureSQLDatabase
from core.models import UserOrm, AccountOrm
from core.security import check_password, generate_tokens, hash_password, validate_token, refresh_access_token
from api.api_utils import parse_request_body, api_error_handler, return_server_error

db = AzureSQLDatabase()
blueprint = func.Blueprint()

@blueprint.route(route="signup", auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
def signup(req: func.HttpRequest) -> func.HttpResponse:
    req_body = parse_request_body(req)

    if db.exists(UserOrm, {"email": req_body['email']}):
        return return_server_error("Email already exists.", status_code=400)

    account = AccountOrm(
        email=req_body['email'],
        password=hash_password(req_body['password']),
    )

    user = UserOrm(
        email=req_body['email'],
        phone=req_body['phone'],
        first_name=req_body['first_name'],
        middle_name=req_body['middle_name'],
        last_name=req_body['last_name'],
    )

    db.insert(user)
    db.insert(account)
    
    access_token, refresh_token = generate_tokens(user.email)
    return func.HttpResponse(
        body=json.dumps({'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()}),
        status_code=200,
        mimetype="application/json"
    )

@blueprint.route(route="signin", auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
def signin(req: func.HttpRequest) -> func.HttpResponse:
    req_body = parse_request_body(req)

    if not db.exists(UserOrm, {"email": req_body['email']}):
        return return_server_error("An account with this email does not exist.", status_code=400)

    account = db.query(AccountOrm, {"email": req_body['email']})[0]
    

    if not check_password(account.password, req_body['password']):
        return_server_error("Incorrect password.", status_code=400)

    user = db.query(UserOrm, {"email": req_body['email']})[0]

    access_token, refresh_token = generate_tokens(user.email)
    return func.HttpResponse(
        body=json.dumps({'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()}),
        status_code=200,
        mimetype="application/json"
    )

@blueprint.route(route="authenticate_token", auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
def authenticate_token(req: func.HttpRequest) -> func.HttpResponse:
    access_token = req.headers.get('Authorization', '').split(' ')[1]
    if not access_token:
        return_server_error("No access token provided.", status_code=401)

    try:
        email = validate_token(access_token)
        user = db.query(UserOrm, {"email": email})[0]
        return func.HttpResponse(
            body=json.dumps({'user': user.to_dict()}),
            status_code=200,
            mimetype="application/json"
        )
    except ValueError as e:
        return_server_error(str(e), status_code=401)

@blueprint.route(route="refresh_token", auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
def refresh_token(req: func.HttpRequest) -> func.HttpResponse:
    refresh_token = req.headers.get('Authorization', '').split(' ')[1]
    if not refresh_token:
        return_server_error("No refresh token provided.", status_code=401)

    try:
        access_token, new_refresh_token = refresh_access_token(refresh_token)
        return func.HttpResponse(
            body=json.dumps({'access_token': access_token, 'refresh_token': new_refresh_token}),
            status_code=200,
            mimetype="application/json"
        )
    except ValueError as e:
        return_server_error(str(e), status_code=401)
