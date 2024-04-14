from pydantic import BaseModel

class Property(BaseModel):
    # Add attributes typically found on MLS listings
    notes: str = None