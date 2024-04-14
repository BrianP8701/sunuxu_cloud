from pydantic import BaseModel, Optional

class APIError(BaseModel):
    code: int
    message: str
    data: Optional[dict] = {}
