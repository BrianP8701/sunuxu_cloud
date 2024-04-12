from pydantic import BaseModel
from typing import Dict, Optional
from enum import Enum

class Person(BaseModel):
    """
    Non transaction specific person model
    """
    id: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: str
    phone: int
    language: str
    transactions: Dict[str, str]

"""
Its important to note that a 'ROLE' class is not necessarily tied to a person
A role is transaction specific and points to a participant class
There also needs to be a clear distinction between transaction transient data and global data per person
For example, if a piece of global data is changed in a transaction it should update all other participant and person models that represent the same person
"""



class Role(Enum):
    SELLER = "seller"
    BUYER = "buyer"
    SELLER_AGENT = "seller_agent"
    BUYER_AGENT = "buyer_agent"
    DUAL_AGENT = "dual_agent"

class Seller(Person):
    pass