from faker import Faker
from typing import Dict, Any, List
import random

from core.enums import TeamRole, State, Brokerage

fake = Faker()

def fake_team_data(user_ids: List[int]) -> Dict[str, Any]:
    admin_id = random.choice(user_ids)
    user_ids.remove(admin_id)
    users = {
        id: fake.random_element(elements=[TeamRole.broker, TeamRole.agent]).value 
        for id in user_ids
    }
    users[admin_id] = TeamRole.admin.value
    return {
        "name": fake.company(),
        "state": random.choice(list(State)).value,  # Ensure valid state value
        "office_address": fake.address(),
        "brokerage": random.choice(list(Brokerage)).value,  # Ensure valid brokerage value
        "users": users
    }
    