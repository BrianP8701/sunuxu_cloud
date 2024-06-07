from faker import Faker
from typing import Dict, Any

from core.utils.security import hash_password

fake = Faker()

def fake_user_data(email: str = None) -> Dict[str, Any]:
    return {
        "email": fake.email() if email is None else email,
        "phone": fake.numerify(text="##########"),
        "first_name": fake.first_name(),
        "middle_name": fake.first_name() if fake.boolean() else None,
        "last_name": fake.last_name(),
        "password": hash_password("password"),
    }
