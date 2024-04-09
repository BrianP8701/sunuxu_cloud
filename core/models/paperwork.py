from pydantic import BaseModel
from typing import Dict, List

class Paperwork(BaseModel):
    """
    This model represents a paperwork object. Paperwork corresponds to a pdf and
    all the fillable fields in the pdf.
    """
    paperwork_id: int
    name: str
    description: str
    # Find descriptions for each field in the Paperwork Field Dictionary
    fields: List[str] # List of field names


class PaperworkStage(BaseModel):
    """
    PaperworkStage represents a stage in the paperwork process, defining
    which fields are required to be filled out and field default values.
    """
    paperwork_stage_id: int
    paperwork_id: int
    required_fields: List[str] # List of required field names
    # required fields cannot have default values
    default_values: Dict[str, str] # Dict[field_name, default_value]
"""
Now theres some problems with the above model.
The required and default fields are not exactly tied to the paperwork class.

For example, with the Sale Listing Package, we undergo phases:
1. First, before signing the contract with the seller we fill out only a few specified fields.
2. Later when we have a signed contract we can update and fill out some other fields (listing period, listing price, etc.)
3. At the end at sale we can fill out the final fields

so we acc should have the paperwork model without the required_fields and default_values fields
we should have a seperate model for the fields that are required and default values at different stages of the paperwork

in addition paperwork can be filled out from different perspectives. for example, it could be a dual agent situation, different compensation.
but all this stuff is stored in the transaction object. so look heres how it works. throughout the process of a transaction the paperwork is filled out
by passing all objects in context and mapping the 
"""