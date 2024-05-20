from enum import Enum


class PropertyType(Enum):
    RESIDENTIAL = "residential"
    CONDO = "condo"
    COOP = "coop"
    COMMERCIAL = "commercial"
    LAND = "land"
    INDUSTRIAL = "industrial"
    RENTAL = "rental"
    CUSTOM = "custom"
    UNKNOWN = "unknown"
