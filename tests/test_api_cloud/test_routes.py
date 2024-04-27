# tests/test_api_cloud/test_routes.py
# pytest tests/test_api_cloud/test_routes.py
import requests
import pytest

from core.database import AzureSQLDatabase
from tests.test_api_cloud.utils import get_function_url

db = AzureSQLDatabase()

def test_signup():
    url = get_function_url("authentication/signup")
    data = {
        "email": "test@example.com",
        "password": "testpassword",
        "phone": "1234567890",
        "first_name": "Test",
        "middle_name": "",
        "last_name": "User",
        "user_type": "agent"
    }

    try:
        response = requests.post(url, json=data)
        assert response.status_code == 200

        response_data = response.json()
        assert "access_token" in response_data
        assert "refresh_token" in response_data
        assert "user" in response_data
        assert response_data["user"]["email"] == "test@example.com"
        assert response_data["user"]["user_type"] == "agent"

        print("test_signup passed")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if response:
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
        raise

def test_signin():
    url = get_function_url("authentication/signin")
    data = {
        "email": "test@example.com",
        "password": "testpassword"
    }

    try:
        response = requests.post(url, json=data)
        assert response.status_code == 200

        response_data = response.json()
        assert "access_token" in response_data
        assert "refresh_token" in response_data
        assert "user" in response_data
        assert response_data["user"]["email"] == "test@example.com"
        assert response_data["user"]["user_type"] == "agent"

        print("test_signin passed")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if response:
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
        raise

def test_delete_user():
    url = get_function_url("sunuxu/admin/delete_user")
    data = {
        "email": "test@example.com"
    }

    try:
        response = requests.post(url, json=data)
        assert response.status_code == 200

        print("test_delete_user passed")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if response:
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
        raise

@pytest.fixture(scope="module", autouse=True)
def clear_database():
    yield
    db.clear_database("I understand this will delete all data")
