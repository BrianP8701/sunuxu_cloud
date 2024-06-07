from enum import Enum


class PersonType(Enum):
    lead = "lead"
    cold_lead = "cold_lead"
    prospect = "prospect"
    client = "client"
    past_client = "past_client"
    agent = "agent"
    broker = "broker"
    attorney = "attorney"
    lender = "lender"
    contractor = "contractor"
    inspector = "inspector"
    appraiser = "appraiser"
    title_officer = "title_officer"
    custom = "custom"
    unknown = "unknown"
