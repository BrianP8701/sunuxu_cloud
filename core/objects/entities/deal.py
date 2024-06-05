from core.models.associations import UserDealAssociation
from core.models.entities.deal import DealModel
from core.objects.base_entities.deal import BaseDeal


class Deal(BaseDeal):
    def _create_new_deal_details_orm(self, propert_id, person_id):
        """
        Create a new deal details object, retrieving either the corresponing person or property.

        """
        deal_details_data = {
            "transaction_platform": self.transaction_platform,
            "notes": self.notes,
        }

        user_associations = [
            UserDealAssociation(user_id=user_id, deal_id=self.id)
            for user_id in self.user_ids
        ]
        deal_details_data["users"] = user_associations

        return DealModel(**deal_details_data)
