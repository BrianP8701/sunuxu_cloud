import json
import azure.functions as func
from api.authentication import signup, login, authenticate_user
from sunuxu.database import AzureSQLDatabase

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
    req = func.HttpRequest(
        method="POST",
        body=json.dumps(req_body).encode("utf-8"),
        url="/api/authentication/signup"  # Add the missing url argument
    )

    # Call the signup function
    response = signup(req)

    # Assert the response status code and content
    assert response.status_code == 200
    assert json.loads(response.get_body())["user"]["username"] == "testuser"

def test_login():
    # Create a test user
    test_signup()

    # Create a mock HTTP request for login
    req_body = {
        "username": "testuser",
        "password": "testpassword"
    }
    req = func.HttpRequest(
        method="POST",
        body=json.dumps(req_body).encode("utf-8"),
        url="/api/authentication/login"  # Add the missing url argument
    )

    # Call the login function
    response = login(req)

    # Assert the response status code and content
    assert response.status_code == 200
    assert "access_token" in json.loads(response.get_body())
    assert "refresh_token" in json.loads(response.get_body())

def test_authenticate_user():
    # Create a test user
    test_signup()

    # Get the access token
    req_body = {
        "username": "testuser",
        "password": "testpassword"
    }
    req = func.HttpRequest(
        method="POST",
        body=json.dumps(req_body).encode("utf-8"),
        url="/api/authentication/login"  # Add the missing url argument
    )
    response = login(req)
    access_token = json.loads(response.get_body())["access_token"]

    # Create a mock HTTP request with the access token
    headers = {
        "Authorization": access_token
    }
    req = func.HttpRequest(
        method="GET",
        headers=headers,
        url="/api/some_authenticated_route"  # Add the missing url argument
    )

    # Define a test function that requires authentication
    @authenticate_user
    def test_authenticated_function(req):
        return func.HttpResponse("Authenticated")

    # Call the test function with authentication
    response = test_authenticated_function(req)

    # Assert the response status code and content
    assert response.status_code == 200
    assert response.get_body() == b"Authenticated"

    # Clear the database after running the tests
    db.clear_database("I understand this will delete all data")

