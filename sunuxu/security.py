# core/security.py
import bcrypt
import base64
from datetime import datetime, timedelta
import jwt
from functools import wraps
import os
import json


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return base64.b64encode(hashed).decode("utf-8")

def check_password(hashed_password: str, user_password: str) -> bool:
    hashed_password_bytes = base64.b64decode(hashed_password.encode("utf-8"))
    return bcrypt.checkpw(user_password.encode("utf-8"), hashed_password_bytes)

def generate_tokens(user_id: str):
    access_token_payload = {
        'user_id': user_id,
        'exp': datetime.now() + timedelta(minutes=15),
        'iat': datetime.now()
    }
    refresh_token_payload = {
        'user_id': user_id,
        'exp': datetime.now() + timedelta(days=7),
        'iat': datetime.now()
    }
    access_token = jwt.encode(access_token_payload, os.getenv("JWT_SECRET"), algorithm='HS256')
    refresh_token = jwt.encode(refresh_token_payload, os.getenv("JWT_SECRET"), algorithm='HS256')
    return access_token, refresh_token

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
                payload = jwt.decode(access_token, os.getenv("JWT_SECRET"), algorithms=['HS256'])
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
