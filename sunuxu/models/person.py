from pydantic import BaseModel
from typing import Dict, Optional

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
