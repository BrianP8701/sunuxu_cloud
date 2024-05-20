from enum import Enum

class ParticipantRole(Enum):
    BUYER = "buyer"
    SELLER = "seller"
    TENANT = "tenant"
    LANDLORD = "landlord"
    BUYER_AGENT = "buyer_agent"
    SELLER_AGENT = "seller_agent"
    DUAL_AGENT = "dual_agent"
    BUYER_ATTORNEY = "buyer_attorney"
    SELLER_ATTORNEY = "seller_attorney"
    DUAL_ATTORNEY = "dual_attorney"
    BUYER_BROKER = "buyer_broker"
    SELLER_BROKER = "seller_broker"
    DUAL_BROKER = "dual_broker"
    LENDER = "lender"
    CONTRACTOR = "contractor"
    INSPECTOR = "inspector"
    APPRAISER = "appraiser"
    TITLE_OFFICER = "title_officer"
    PROPERTY_MANAGER = "property_manager"
    CUSTOM = "custom"
    UNKNOWN = "unknown"
