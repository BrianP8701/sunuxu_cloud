from pydantic import BaseModel
from typing import Optional

class APIError(BaseModel):
    code: int
    message: str
    data: Optional[dict] = {}
