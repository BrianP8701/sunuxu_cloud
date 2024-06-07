from enum import Enum


class PropertyType(Enum):
    residential = "residential"
    condo = "condo"
    coop = "coop"
    commercial = "commercial"
    land = "land"
    industrial = "industrial"
    rental = "rental"
    custom = "custom"
    unknown = "unknown"
