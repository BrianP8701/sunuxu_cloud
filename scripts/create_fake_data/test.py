import faker
import asyncio
from pydantic import BaseModel

from core.objects.entities.user import User
from core.objects.entities.person import Person
from core.enums.person_type import PersonType
from core.integrations.instructor import Instructor
from tests.utils.generate_test_data.simulate_conversation import simulate_conversation

faker = faker.Faker()

user = User(
    id=1,
    email="brian@brianhayes.dev",
    phone="+1234567890",
    first_name="Brian",
    last_name="Hayes",
    password="password"
)

person = Person(
    id=1,
    user_ids=[],
    name="John Doe",
    first_name="John",
    last_name="Doe",
    middle_name="Smith",
    active=False,
    email="john.doe@example.com",
    phone="+1234567890",
    language="English",
    # type=faker.random_element(elements=PersonType),
    type=PersonType.ATTORNEY,
    users=[]
)

response = asyncio.run(simulate_conversation(user, person, 10, 50))

print(response)
