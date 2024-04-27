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

def validate_token(token: str, is_access_token: bool = True) -> str:
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        if is_access_token:
            raise ValueError("Access token expired.")
        else:
            raise ValueError("Refresh token expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token.")

def refresh_access_token(refresh_token: str):
    try:
        user_id = validate_token(refresh_token, is_access_token=False)
        return generate_tokens(user_id)
    except ValueError as e:
        raise ValueError(str(e))
