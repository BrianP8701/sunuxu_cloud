# api/authentication/signup/main.py
import azure.functions as func
import json

from core.database import AzurePostgreSQLDatabase
from core.models import UserOrm
from core.security import generate_tokens, hash_password
from api.api_utils import parse_request_body, api_error_handler, return_server_error

blueprint = func.Blueprint()

@blueprint.route(route="signup", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
async def signup(req: func.HttpRequest) -> func.HttpResponse:
    db = AzurePostgreSQLDatabase()


    req_body = parse_request_body(req)

    if await db.exists(UserOrm, {"email": req_body['email']}):
        return return_server_error("Email already exists.", status_code=400)

    user = UserOrm(
        email=req_body['email'],
        phone=req_body['phone'],
        first_name=req_body['first_name'],
        middle_name=req_body['middle_name'],
        last_name=req_body['last_name'],
        password=hash_password(req_body['password'])
    )

    await db.insert(user)
    
    access_token, refresh_token = generate_tokens(user.id)
    return func.HttpResponse(
        body=json.dumps({'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()}),
        status_code=200,
        mimetype="application/json"
    )
