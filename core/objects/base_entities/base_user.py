from typing import Any, Dict, Optional

from core.database import Database
from core.enums.deal_platform import DealPlatform
from core.enums.service_connection_status import ServiceConnectionStatus
from core.models import UserRowModel
from core.models.entities.deal import DealModel
from core.models.entities.person import PersonModel
from core.models.entities.property import PropertyModel
from core.models.entities.team import TeamModel
from core.models.entities.user import UserModel
from core.objects.base_entities.base_entity import BaseEntity


class BaseUser(BaseEntity):
    id: Optional[int] = None
    email: str
    phone: Optional[str] = None
    password: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str

    redux_version: Optional[int] = None
    changelog_viewed: Optional[bool] = None
    developer_conversation_viewed: Optional[bool] = None
    signature: Optional[bytes] = None
    forwarding_number: Optional[str] = None
    twilio_phone_number: Optional[str] = None
    twilio_sid: Optional[str] = None
    mls_connected: Optional[bool] = None
    mls_username: Optional[str] = None
    mls_password: Optional[str] = None
    skyslope_connection_status: ServiceConnectionStatus = (
        ServiceConnectionStatus.NOT_CONNECTED
    )
    skyslope_username: Optional[str] = None
    skyslope_password: Optional[str] = None
    idx_website_domain: Optional[str] = None
    mls_connection_status: Optional[ServiceConnectionStatus] = None
    mls_api_connection_status: Optional[ServiceConnectionStatus] = None
    default_mls: Optional[str] = None
    default_deal_platform: Optional[DealPlatform] = None
    default_message_new_leads: Optional[bool] = None
    email_connection_status: Optional[ServiceConnectionStatus] = None
    email_template: Optional[str] = None
    shared_email: Optional[str] = None
    email_access_token: Optional[str] = None
    email_refresh_token: Optional[str] = None
    email_token_expiry: Optional[str] = None
    instagram_connection_status: Optional[ServiceConnectionStatus] = None
    instagram_access_token: Optional[str] = None
    instagram_token_expiry: Optional[str] = None
    linkedin_connection_status: Optional[ServiceConnectionStatus] = None
    linkedin_access_token: Optional[str] = None
    linkedin_token_expiry: Optional[str] = None
    facebook_connection_status: Optional[ServiceConnectionStatus] = None
    facebook_access_token: Optional[str] = None
    facebook_token_expiry: Optional[str] = None
    x_connection_status: Optional[ServiceConnectionStatus] = None
    x_access_token: Optional[str] = None
    x_token_expiry: Optional[str] = None
    google_business_connection_status: Optional[ServiceConnectionStatus] = None
    google_business_access_token: Optional[str] = None
    google_business_token_expiry: Optional[str] = None
    follow_up_boss_connection_status: Optional[ServiceConnectionStatus] = None
    follow_up_boss_access_token: Optional[str] = None
    follow_up_boss_token_expiry: Optional[str] = None
    brivity_connection_status: Optional[ServiceConnectionStatus] = None
    brivity_access_token: Optional[str] = None
    brivity_token_expiry: Optional[str] = None
    kvcore_connection_status: Optional[ServiceConnectionStatus] = None
    kvcore_access_token: Optional[str] = None
    kvcore_token_expiry: Optional[str] = None
    created: Optional[str] = None

    user_orm: Optional[UserRowModel] = None
    user_details_orm: Optional[UserModel] = None

    @classmethod
    async def create(cls, user_id: int, data: Dict[str, Any]) -> "BaseUser":
        db = Database()

        user_row = UserRowModel(
            email=data["email"],
            phone=data.get("phone"),
            first_name=data["first_name"],
            middle_name=data.get("middle_name"),
            last_name=data["last_name"],
        )

        user_details = UserModel(password=data["password"], row=user_row)

        async with db.get_session() as session:
            await db.batch_create([user_row, user_details], session)

        return cls(
            id=user_row.id,
            email=user_row.email,
            phone=user_row.phone,
            first_name=user_row.first_name,
            middle_name=user_row.middle_name,
            last_name=user_row.last_name,
            password=user_details.password,
            user_orm=user_row,
            user_details_orm=user_details,
        )

    @classmethod
    async def read(cls, id: int) -> "BaseUser":
        db = Database()
        user = await db.read(UserRowModel, id, eager_load=["user_details"])
        return cls(
            id=user.id,
            email=user.email,
            phone=user.phone,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            redux_version=user.redux_version,
            changelog_viewed=user.changelog_viewed,
            developer_conversation_viewed=user.developer_conversation_viewed,
            signature=user.signature,
            forwarding_number=user.forwarding_number,
            twilio_phone_number=user.twilio_phone_number,
            twilio_sid=user.twilio_sid,
            mls_connected=user.mls_connected,
            mls_username=user.mls_username,
            mls_password=user.mls_password,
            skyslope_connection_status=user.skyslope_connection_status,
            skyslope_username=user.skyslope_username,
            skyslope_password=user.skyslope_password,
            idx_website_domain=user.idx_website_domain,
            mls_connection_status=user.mls_connection_status,
            mls_api_connection_status=user.mls_api_connection_status,
            default_mls=user.default_mls,
            default_deal_platform=user.default_deal_platform,
            default_message_new_leads=user.default_message_new_leads,
            email_connection_status=user.email_connection_status,
            email_template=user.email_template,
            shared_email=user.shared_email,
            email_access_token=user.email_access_token,
            email_refresh_token=user.email_refresh_token,
            email_token_expiry=user.email_token_expiry,
            instagram_connection_status=user.instagram_connection_status,
            instagram_access_token=user.instagram_access_token,
            instagram_token_expiry=user.instagram_token_expiry,
            linkedin_connection_status=user.linkedin_connection_status,
            linkedin_access_token=user.linkedin_access_token,
            linkedin_token_expiry=user.linkedin_token_expiry,
            facebook_connection_status=user.facebook_connection_status,
            facebook_access_token=user.facebook_access_token,
            facebook_token_expiry=user.facebook_token_expiry,
            x_connection_status=user.x_connection_status,
            x_access_token=user.x_access_token,
            x_token_expiry=user.x_token_expiry,
            google_business_connection_status=user.google_business_connection_status,
            google_business_access_token=user.google_business_access_token,
            google_business_token_expiry=user.google_business_token_expiry,
            follow_up_boss_connection_status=user.follow_up_boss_connection_status,
            follow_up_boss_access_token=user.follow_up_boss_access_token,
            follow_up_boss_token_expiry=user.follow_up_boss_token_expiry,
            brivity_connection_status=user.brivity_connection_status,
            brivity_access_token=user.brivity_access_token,
            brivity_token_expiry=user.brivity_token_expiry,
            kvcore_connection_status=user.kvcore_connection_status,
            kvcore_access_token=user.kvcore_access_token,
            kvcore_token_expiry=user.kvcore_token_expiry,
            created=user.created,
            user_orm=user,
            user_details_orm=user.details,
        )

    @classmethod
    async def update(cls, id: int, updates: Dict[str, Any]):
        db = Database()

        user_updates = {}
        user_details_updates = {}

        for key, value in updates.items():
            if hasattr(UserRowModel, key):
                user_updates[key] = value
            elif hasattr(UserModel, key):
                user_details_updates[key] = value

        async with db.get_session() as session:
            await db.update_fields(UserRowModel, id, user_updates, session)
            await db.update_fields(UserModel, id, user_details_updates, session)

    @classmethod
    async def delete(cls, id: int):
        """
        Delete a user and cascade delete associated entities (teams, people, properties, deals)
        if no other users are associated with them.

        Args:
            id (int): The ID of the user to delete.
        """
        db = Database()

        # SQL query to count the number of users associated with each entity type for the given user
        count_entities_sql = """
        SELECT 'team' AS entity_type, team_id AS entity_id, COUNT(user_id) AS count_of_users
        FROM user_team_association
        WHERE user_id = :user_id
        GROUP BY team_id

        UNION ALL

        SELECT 'person' AS entity_type, person_id AS entity_id, COUNT(user_id) AS count_of_users
        FROM user_person_association
        WHERE user_id = :user_id
        GROUP BY person_id

        UNION ALL

        SELECT 'property' AS entity_type, property_id AS entity_id, COUNT(user_id) AS count_of_users
        FROM user_property_association
        WHERE user_id = :user_id
        GROUP BY property_id

        UNION ALL

        SELECT 'deal' AS entity_type, deal_id AS entity_id, COUNT(user_id) AS count_of_users
        FROM user_deal_association
        WHERE user_id = :user_id
        GROUP BY deal_id;
        """

        # Execute the raw SQL query with the user ID parameter
        entities_result = await db.execute_raw_sql(count_entities_sql, {"user_id": id})

        delete_team_ids = []
        delete_person_ids = []
        delete_deal_ids = []
        delete_property_ids = []

        # Determine which entities should be deleted based on the count of users
        for entity in entities_result:
            if entity.count_of_users == 0:
                if entity.entity_type == "team":
                    delete_team_ids.append(entity.entity_id)
                elif entity.entity_type == "person":
                    delete_person_ids.append(entity.entity_id)
                elif entity.entity_type == "deal":
                    delete_deal_ids.append(entity.entity_id)
                elif entity.entity_type == "property":
                    delete_property_ids.append(entity.entity_id)

        # Perform the deletions in a database session
        async with db.get_session() as session:
            async with session.begin():  # Ensure atomic transaction
                if delete_team_ids:
                    await db.delete_batch(TeamModel, {"id": delete_team_ids}, session)
                if delete_person_ids:
                    await db.delete_batch(
                        PersonModel, {"id": delete_person_ids}, session
                    )
                if delete_deal_ids:
                    await db.delete_batch(DealModel, {"id": delete_deal_ids}, session)
                if delete_property_ids:
                    await db.delete_batch(
                        PropertyModel, {"id": delete_property_ids}, session
                    )
                await db.delete(UserModel, {"id": id}, session)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "redux_version": self.redux_version,
            "changelog_viewed": self.changelog_viewed,
            "developer_conversation_viewed": self.developer_conversation_viewed,
            "signature": self.signature,
            "forwarding_number": self.forwarding_number,
            "twilio_phone_number": self.twilio_phone_number,
            "twilio_sid": self.twilio_sid,
            "mls_connected": self.mls_connected,
            "mls_username": self.mls_username,
            "mls_password": self.mls_password,
            "skyslope_connection_status": self.skyslope_connection_status,
            "skyslope_username": self.skyslope_username,
            "skyslope_password": self.skyslope_password,
            "idx_website_domain": self.idx_website_domain,
            "mls_connection_status": self.mls_connection_status,
            "mls_api_connection_status": self.mls_api_connection_status,
            "default_mls": self.default_mls,
            "default_deal_platform": self.default_deal_platform,
            "default_message_new_leads": self.default_message_new_leads,
            "email_connection_status": self.email_connection_status,
            "email_template": self.email_template,
            "shared_email": self.shared_email,
            "email_access_token": self.email_access_token,
            "email_refresh_token": self.email_refresh_token,
            "email_token_expiry": self.email_token_expiry,
            "instagram_connection_status": self.instagram_connection_status,
            "instagram_access_token": self.instagram_access_token,
            "instagram_token_expiry": self.instagram_token_expiry,
            "linkedin_connection_status": self.linkedin_connection_status,
            "linkedin_access_token": self.linkedin_access_token,
            "linkedin_token_expiry": self.linkedin_token_expiry,
            "facebook_connection_status": self.facebook_connection_status,
            "facebook_access_token": self.facebook_access_token,
            "facebook_token_expiry": self.facebook_token_expiry,
            "x_connection_status": self.x_connection_status,
            "x_access_token": self.x_access_token,
            "x_token_expiry": self.x_token_expiry,
            "google_business_connection_status": self.google_business_connection_status,
            "google_business_access_token": self.google_business_access_token,
            "google_business_token_expiry": self.google_business_token_expiry,
            "follow_up_boss_connection_status": self.follow_up_boss_connection_status,
            "follow_up_boss_access_token": self.follow_up_boss_access_token,
            "follow_up_boss_token_expiry": self.follow_up_boss_token_expiry,
            "brivity_connection_status": self.brivity_connection_status,
            "brivity_access_token": self.brivity_access_token,
            "brivity_token_expiry": self.brivity_token_expiry,
            "kvcore_connection_status": self.kvcore_connection_status,
            "kvcore_access_token": self.kvcore_access_token,
            "kvcore_token_expiry": self.kvcore_token_expiry,
            "created": self.created,
        }
