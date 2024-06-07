from faker import Faker
from typing import Dict, Any, List
from core.enums import DealStatus, DealType, DealCategory, ParticipantRole

fake = Faker()

def fake_deal_data(
    user_ids: List[int], participants: List[int], property_id: int
) -> Dict[str, Any]:
    return {
        "user_ids": user_ids,
        "category": fake.random_element(elements=DealCategory).value,
        "status": fake.random_element(elements=DealStatus).value,
        "type": fake.random_element(elements=DealType).value,
        "participants": {
            id: fake.random_element(elements=ParticipantRole).value
            for id in participants
        },
        "property_id": property_id,
        "transaction_platform": fake.company(),
        "notes": fake.text(max_nb_chars=200),
    }
