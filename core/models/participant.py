from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum

from core.database.abstract import Base

class ParticipantRoleEnum(str, Enum):
    Buyer = "Buyer"
    Seller = "Seller"
    Lender = "Lender"
    Inspector = "Inspector"
    TitleAgent = "Title Agent"
    BuyerAgent = "Buyer's Agent"
    SellerAgent = "Seller's Agent"
    DualAgent = "Dual Agent"
    Appraiser = "Appraiser"
    BuyerAttorney = "Buyer's Attorney"
    SellerAttorney = "Seller's Attorney"
    Photographer = "Photographer"
    Stager = "Stager"
    Contractor = "Contractor"
    EscrowOfficer = "Escrow Officer"
    MortgageBroker = "Mortgage Broker"
    PropertyManager = "Property Manager"
    Landlord = "Landlord"
    Renter = "Renter"
    Tenant = "Tenant"
    InsuranceAgent = "Insurance Agent"
    ReferralAgent = "Referral Agent"
    ClosingAgent = "Closing Agent"
    Surveyor = "Surveyor"
    HomeWarrantyAgent = "Home Warranty Agent"
    Other = "Other"

class ParticipantOrm(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True)
    participant_id = Column(String)
    person_id = Column(String)
    transaction_id = Column(String)
    role = Column(SQLEnum(ParticipantRoleEnum))
    relationships = Column(String)  # Store relationships as JSON string
