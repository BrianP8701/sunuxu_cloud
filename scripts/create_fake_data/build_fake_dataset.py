"""
Script to generate and persist a dataset locally.

This is fake data used to test our application.
"""
import os
import json
import random
import asyncio

from scripts.create_fake_data.simulate_conversation import batch_simulate_conversation
from scripts.create_fake_data.fake_deal import fake_deal_data
from scripts.create_fake_data.fake_person import fake_person_data
from scripts.create_fake_data.fake_property import fake_property_data
from scripts.create_fake_data.fake_user import fake_user_data 
from scripts.create_fake_data.fake_team import fake_team_data

from core.utils.ids import cantor_pairing
from core.objects.entities import User, Person, Property, Team, Deal, Message

"""
Things our current fake dataset doesn't cover:
- Email threads
- Developer messages
- Changelog
- Team messages
- Notes
"""

async def create_and_persist_fake_dataset(user_count: int = 7, team_count: int = 3, people_count: int = 1000, property_count: int = 500, deal_count: int = 100):
    """
    Build and organize a fake dataset.
    
    Create conversations for the first user's people.
    """
    # Create fake users
    user_data = [fake_user_data() for _ in range(user_count)]
    users = await User.batch_create(user_data)
    
    # To keep track of first users people
    first_user_people = []

    # Initialize the raw data dictionary
    raw_data = {
        'users': user_data,
        'teams': [],
        'people': [],
        'properties': [],
        'deals': [],
        'messages': []
    }

    # Create fake teams
    for _ in range(team_count):
        user_ids = random.sample(users, random.randint(1, user_count))
        team_data = fake_team_data([user.id for user in users])
        raw_data['teams'].append(team_data)
    teams = await Team.batch_create(raw_data['teams'])

    # Create fake people and associate them with users
    first_user_people_indices = []
    for _ in range(people_count):
        users = random.sample(users, random.randint(1, user_count))
        user_ids = [user.id for user in users]
        if users[0].id in user_ids:
            first_user_people.append(_)
        raw_data['people'].extend(fake_person_data(user_ids))
    people = await Person.batch_create(raw_data['people'])
    first_user_people = [people[i] for i in first_user_people_indices]

    # Create fake properties and associate them with users and people
    for _ in range(property_count):
        users = random.sample(users, random.randint(1, user_count))
        owners = random.sample(people, random.randint(1, people_count))
        occupants = random.sample(people, random.randint(1, people_count))
        property_data = fake_property_data([user.id for user in users], [person.id for person in owners], [person.id for person in occupants])
        properties = await Property.batch_create(property_data)
        raw_data['properties'].extend(property_data)
    properties = await Property.batch_create(raw_data['properties'])

    # Create fake deals and associate them with users, people, and properties
    for _ in range(deal_count):
        users = random.sample(users, random.randint(1, user_count))
        property = random.choice(properties)
        people = random.sample(people, random.randint(1, people_count))
        deal_data = fake_deal_data([user.id for user in users], property.id, [person.id for person in people])
        raw_data['deals'].extend(deal_data)
    deals = await Deal.batch_create(raw_data['deals'])

    conversations = await batch_simulate_conversation(users[0], people)
    for i, conversation in enumerate(conversations):
        for message in conversation.messages:
            message_dict = {
                "type": 'email' if message.email_subject else 'sms',
                "role": message.role.value,
                "user_id": users[0].id,
                "source_id": cantor_pairing(users[0].id, people[i].id),
                "source_type": 'person',
                "content": message.content,
                "from_number": users[0].phone_number if not message.email_subject else None,
                "to_number": people[i].phone_number if not message.email_subject else None,
                "from_email": users[0].email if message.email_subject else None,
                "recipient_email": people[i].email if message.email_subject else None,
                "email_subject": message.email_subject if message.email_subject else None,
            }
            raw_data['messages'].append(message_dict)
    messages = await Message.batch_create(raw_data['messages'])

    dataset_dir = 'scripts/create_fake_data/fake_datasets'
    os.makedirs(dataset_dir, exist_ok=True)

    file_index = 0
    while os.path.exists(os.path.join(dataset_dir, f'fake_dataset_{file_index}.json')):
        file_index += 1

    dataset_path = os.path.join(dataset_dir, f'fake_dataset_{file_index}.json')
    with open(dataset_path, 'w') as f:
        json.dump(raw_data, f, indent=4)

    print(f"Dataset saved to {dataset_path}")


if __name__ == '__main__':
    asyncio.run(create_and_persist_fake_dataset())

