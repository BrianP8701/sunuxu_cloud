# api/authentication.py
import azure.functions as func
import bcrypt
import base64
import json
from datetime import datetime, timedelta
import jwt
from functools import wraps
import os

from sunuxu.database import AzureSQLDatabase
from sunuxu.models import UserOrm

db = AzureSQLDatabase()
bp = func.Blueprint()

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return base64.b64encode(hashed).decode("utf-8")

def check_password(hashed_password: str, user_password: str) -> bool:
    hashed_password_bytes = base64.b64decode(hashed_password.encode("utf-8"))
    return bcrypt.checkpw(user_password.encode("utf-8"), hashed_password_bytes)

def generate_tokens(user_id: str):
    access_token_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iat': datetime.utcnow()
    }
    refresh_token_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    access_token = jwt.encode(access_token_payload, 'your_secret_key', algorithm='HS256')
    refresh_token = jwt.encode(refresh_token_payload, 'your_secret_key', algorithm='HS256')
    return access_token, refresh_token

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


def authenticate_user(func):
    """
    Decorator function to authenticate user using JWT tokens.
    """
    @wraps(func)
    def wrapper(req: func.HttpRequest, *args, **kwargs):
        access_token = req.headers.get('Authorization')
        if not access_token:
            refresh_token = req.headers.get('Refresh-Token')
            if not refresh_token:
                return func.HttpResponse(
                    json.dumps({'error': 'No token provided.'}),
                    status_code=401,
                    mimetype='application/json'
                )
            try:
                payload = jwt.decode(refresh_token, os.getenv("JWT_SECRET"), algorithms=['HS256'])
                user_id = payload['user_id']
                access_token, refresh_token = generate_tokens(user_id)
                kwargs['user_id'] = user_id
                req.headers['Authorization'] = access_token
                req.headers['Refresh-Token'] = refresh_token
                return func(req, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return func.HttpResponse(
                    json.dumps({'error': 'Refresh token expired.'}),
                    status_code=401,
                    mimetype='application/json'
                )
        else:
            try:
                payload = jwt.decode(access_token, 'your_secret_key', algorithms=['HS256'])
                user_id = payload['user_id']
                kwargs['user_id'] = user_id
                return func(req, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return func.HttpResponse(
                    json.dumps({'error': 'Access token expired.'}),
                    status_code=401,
                    mimetype='application/json'
                )
    return wrapper
