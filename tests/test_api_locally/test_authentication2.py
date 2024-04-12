import json
import azure.functions as func
from azure.functions import HttpRequest
from api.authentication import app
from app.database import AzureSQLDatabase

db = AzureSQLDatabase()

def test_signup():
    # Clear the database before running the test
    db.clear_database("I understand this will delete all data")

    # Create a mock HTTP request for signup
    req_body = {
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com",
        "phone": "1234567890",
        "first_name": "Test",
        "last_name": "User",
        "user_type": "customer"
    }

    # Call the function app with the request
    response = app.test_client().post("/api/authentication/signup", data=req_body)

    # Assert the response status code and content
    assert response.status_code == 200
    assert json.loads(response.get_data())["user"]["username"] == "testuser"

def test_login():
    # Create a test user
    test_signup()

    # Create a mock HTTP request for login
    req_body = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Call the function app with the request
    response = app.test_client().post("/api/authentication/login", data=req_body)

    # Assert the response status code and content
    assert response.status_code == 200
    assert "access_token" in json.loads(response.get_data())
    assert "refresh_token" in json.loads(response.get_data())
