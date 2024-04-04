from pydantic import BaseModel
from typing import List

class BasePlan(BaseModel):
    # Add common fields for all plans
    pass

class ConvertLeadPlan(BasePlan):
    # Add fields specific to converting leads
    pass


class CategorizePersonPlan(BasePlan):
    # Add fields specific to categorizing persons
    pass

class SellerPlan(BasePlan):
    # Add fields specific to seller interactions
    pass

class BuyerPlan(BasePlan):
    # Add fields specific to buyer interactions
    pass

class SellerLawyerPlan(BasePlan):
    # Add fields specific to seller's lawyer interactions
    pass
