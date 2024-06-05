# tests/test_api_locally/test_routes.py
# pytest -s tests/test_api/test_authentication.py
import pytest
import requests

from core.database import Database
from core.models import UserRowModel
from tests.utils.get_url import get_function_url

db = Database()


def test_signup():
    url = get_function_url("signup")
    data = {
        "email": "test@example.com",
        "password": "testpassword",
        "phone": "1234567890",
        "first_name": "Test",
        "middle_name": "",
        "last_name": "User",
    }

    try:
        response = requests.post(url, json=data)
        assert response.status_code == 200

        response_data = response.json()
        assert "access_token" in response_data
        assert "refresh_token" in response_data
        assert "user" in response_data
        assert response_data["user"]["email"] == "test@example.com"

        print("test_signup passed")
    except:
        print(f"Request failed: {response}")
        if response:
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
        raise


def test_signin():
    url = get_function_url("signin")
    data = {"email": "test@example.com", "password": "testpassword"}

    try:
        response = requests.post(url, json=data)
        assert response.status_code == 200

        response_data = response.json()
        assert "access_token" in response_data
        assert "refresh_token" in response_data
        assert "user" in response_data
        assert response_data["user"]["email"] == "test@example.com"

        print("test_signin passed")
    except:
        print(f"Request failed: {response}")
        if response:
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
        raise


def test_delete_user():
    url = get_function_url("sunuxu/admin/delete_user")
    data = {"email": "test@example.com"}

    try:
        response = requests.delete(url, json=data)
        assert response.status_code == 200

        print("test_delete_user passed")
    except:
        print(f"Request failed: {response}")
        if response:
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
        raise


@pytest.fixture(scope="module", autouse=True)
async def clear_database():
    yield
    if await db.exists(UserRowModel, {"email": "test@example.com"}):
        await db.delete(UserRowModel, {"email": "test@example.com"})
    db.dispose_instance()
