from typing import Dict, Any, List
from faker import Faker

from core.enums import PersonType

fake = Faker()

def fake_person_data(
    user_ids: List[int], residence_id: int, portfolio_ids: List[int]
) -> Dict[str, Any]:
    """
    Generates a dictionary of person data using Faker.

    :param user_id:
        The ID of the user creating the person.
    :return:
        A dictionary containing the person details.
    """
    return {
        "user_ids": user_ids,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "middle_name": fake.first_name() if fake.boolean() else None,
        "email": fake.email(),
        "phone": fake.phone_number(),
        "type": fake.random_element(elements=PersonType).value,
        "language": fake.language_name(),
        "residence_id": residence_id,
        "portfolio_ids": portfolio_ids,
    }
