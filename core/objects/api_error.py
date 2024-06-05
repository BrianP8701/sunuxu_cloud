from typing import Optional

from pydantic import BaseModel


class APIError(BaseModel):
    code: int
    message: str
    data: Optional[dict] = {}
