from typing import List, Union
from pydantic import BaseModel, Field
import random
import asyncio

from core.integrations.instructor import Instructor
from core.objects.entities.user import User
from core.objects.entities.person import Person
from core.enums.message_role import MessageRole


instructor = Instructor()

class Message(BaseModel):
    role: MessageRole
    content: str

class EmailMessage(Message):
    email_subject: str

class Conversation(BaseModel):
    messages: List[Union[Message, EmailMessage]] = Field(
        ...,
        description=(
            "List of messages."
        )
    )


async def simulate_conversation(user: User, person: Person, length: int, scuffed_meter: int) -> Conversation:
    """
    Generates a synthetic conversation between a real estate agent and a person.

    :param person: Metadata about the person.
    :param length: Number of messages.
    :param scuffed_meter: Quality of communication (1-100, 0 being the poorest).
    :return: A Conversation object.
    """

    generate_conversation_prompt = f"""
    Generate a synthetic conversation between a real estate agent and a person.
    Details:
    - Person named {person.name}. The person is a {person.type}.
    - Agent {user.first_name} {user.last_name}.
    - On a range from 0-100, where 0 means the communication from the person is awful and 100 means the person is perfect, the conversation is {scuffed_meter} scuffed.
    - Conversation length: {length} messages.
    - Agent remains professional, style may vary.
    
    The conversation should be realistic, it doesen't have to finish, people can double text, they may be familiar with each other, hop between text and email, etc.
    """

    response = await instructor.completion(
        messages=[{"role": "system", "content": generate_conversation_prompt}],
        response_model=Conversation,
        temperature=0.8,
        max_retries=10
    )

    return response

async def batch_simulate_conversation(user: User, people: List[Person], min_messages: int = 3, max_messages: int = 20, min_scuffed_meter: int = 0, max_scuffed_meter: int = 100) -> List[Conversation]:
    conversations = []
    for person in people:
        length = random.randint(min_messages, max_messages)
        scuffed_meter = random.randint(min_scuffed_meter, max_scuffed_meter)
        conversation = simulate_conversation(user, person, length, scuffed_meter)
        conversations.append(conversation)
    
    await asyncio.gather(*[simulate_conversation(user, person, length, scuffed_meter) for person in people])

    return conversations
