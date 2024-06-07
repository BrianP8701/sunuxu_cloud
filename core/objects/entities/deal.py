from typing import Any, Dict, List

from core.database import Database
from core.enums import DealCategory, DealStatus, DealType, ParticipantRole
from core.models.associations import UserDealAssociation, DealParticipantAssociation
from core.models.entities.deal import DealModel
from core.models.rows.person import PersonRowModel
from core.models.rows.property import PropertyRowModel
from core.models.rows.deal import DealRowModel
from core.objects.base_entities.base_deal import BaseDeal


class Deal(BaseDeal):
   pass