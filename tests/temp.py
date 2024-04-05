# temporary test file to fuck around
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from typing import Optional
from enum import Enum
import os
import json
import azure.functions as func
from api.authentication import signup, login, authenticate_user
from core.database import AzureSQLDatabase
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from pydantic import BaseModel, ConfigDict

# Create the connection string
req_body = {
    "username": "testuser",
    "password": "testpassword",
    "email": "test@example.com",
    "phone": "1234567890",
    "first_name": "Test",
    "last_name": "User",
    "user_type": "customer"
}
req = func.HttpRequest(
    method="POST",
    body=json.dumps(req_body).encode("utf-8"),
    url="/api/authentication/signup"  # Add the missing url argument
)

# Call the signup function
response = signup(req)

print(response)