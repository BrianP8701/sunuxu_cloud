from typing import List, Optional, Dict, Any

from core.database import Database
from core.models import UserRowOrm
from core.models.entities.user import UserOrm
from core.objects.objects.base_object import BaseObject
from core.enums.deal_platform import DealPlatform
from core.enums.service_connection_status import ServiceConnectionStatus
from core.models.entities.person import PersonOrm
from core.models.entities.property import PropertyOrm
from core.models.entities.deal import DealOrm
from core.models.entities.team import TeamOrm

class User(BaseObject):
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
    skyslope_connection_status: ServiceConnectionStatus = ServiceConnectionStatus.NOT_CONNECTED
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

    user_orm: Optional[UserRowOrm] = None
    user_details_orm: Optional[UserOrm] = None

    @classmethod
    async def read(cls, id: int) -> "User":
        db = Database()
        user = await db.read(UserRowOrm, id, eager_load=["user_details"])
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
            user_details_orm=user.details
        )

    async def create(self) -> "User":
        if self.id:
            raise ValueError("User already exists")
        db = Database()

        user_orm, user_details_orm = self._assemble_orm()

        async with db.get_session() as session:
            await db.batch_create([user_orm, user_details_orm], session)
        self.id = user_orm.id
        self.user_orm = user_orm
        self.user_details_orm = user_details_orm

    @classmethod
    async def update(cls, id: int, updates: Dict[str, Any]):
        db = Database()
        
        user_updates = {}
        user_details_updates = {}
        
        for key, value in updates.items():
            if hasattr(UserRowOrm, key):
                user_updates[key] = value
            elif hasattr(UserOrm, key):
                user_details_updates[key] = value

        async with db.get_session() as session:
            await db.update_fields(UserRowOrm, id, user_updates, session)
            await db.update_fields(UserOrm, id, user_details_updates, session)

    @classmethod
    async def batch_read(cls, user_ids: List[int]) -> List["User"]:
        db = Database()
        users = await db.batch_query(UserRowOrm, {"id": user_ids})
        return [cls(**user.to_dict()) for user in users]

    @classmethod
    async def delete(cls, id: int):
        """
        Teams enable some objects to have multiple users, meaning we can't just cascade deletes.
        In this method we check all the users objects and delete them if they no longer have any users.
        
        So we'll want to fetch all the people, properties, deals associated with a user, check if the users list is empty and delete if so.
        Those will cascade deletes accordingly to their relationships
        """
        db = Database()

        people_sql = """
        SELECT p.id AS person_id, p.user_ids AS person_user_ids
        FROM user_person_association upa
        LEFT JOIN person_details pd ON upa.person_id = pd.id
        LEFT JOIN people p ON pd.id = p.id
        WHERE upa.user_id = :user_id;
        """
        deals_sql = """
        SELECT d.id AS deal_id, d.user_ids AS deal_user_ids
        FROM user_deal_association uda
        LEFT JOIN deal_details dd ON uda.deal_id = dd.id
        LEFT JOIN deals d ON dd.id = d.id
        WHERE uda.user_id = :user_id;
        """
        properties_sql = """
        SELECT pr.id AS property_id, pr.user_ids AS property_user_ids
        FROM user_property_association upra
        LEFT JOIN property_details prd ON upra.property_id = prd.id
        LEFT JOIN properties pr ON prd.id = pr.id
        WHERE upra.user_id = :user_id;
        """
        teams_sql = """
        SELECT td.id AS team_id, td.user_ids AS team_user_ids
        FROM user_team_association uta
        LEFT JOIN team_details td ON uta.team_id = td.id
        WHERE uta.user_id = :user_id;
        """

        async with db.get_session() as session:
            people_result = await db.execute_raw_sql(people_sql, {"user_id": id}, session)
            deals_result = await db.execute_raw_sql(deals_sql, {"user_id": id}, session)
            properties_result = await db.execute_raw_sql(properties_sql, {"user_id": id}, session)
            teams_result = await db.execute_raw_sql(teams_sql, {"user_id": id}, session)


        delete_person_ids = []
        delete_deal_ids = []
        delete_property_ids = []
        delete_team_ids = []

        for person_id, person_user_ids in people_result:
            if not person_user_ids:
                delete_person_ids.append(person_id)
        for deal_id, deal_user_ids in deals_result:
            if not deal_user_ids:
                delete_deal_ids.append(deal_id)
        for property_id, property_user_ids in properties_result:
            if not property_user_ids:
                delete_property_ids.append(property_id)
        for team_id, team_user_ids in teams_result:
            if not team_user_ids:
                delete_team_ids.append(team_id)

        async with db.get_session() as session:
            await db.delete_batch(PersonOrm, {"id": delete_person_ids}, session)
            await db.delete_batch(DealOrm, {"id": delete_deal_ids}, session)
            await db.delete_batch(PropertyOrm, {"id": delete_property_ids}, session)
            await db.delete_batch(TeamOrm, {"id": delete_team_ids}, session)
            await db.delete(UserOrm, {"id": id}, session)

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
            "custom_person_types": self.custom_person_types,
            "custom_property_types": self.custom_property_types,
            "custom_transaction_types": self.custom_transaction_types,
            "custom_transaction_statuses": self.custom_transaction_statuses,
            "custom_participant_roles": self.custom_participant_roles
        }

    def _assemble_orm(self):
        user = UserRowOrm(
            password=self.password,
            email=self.email,
            phone=self.phone,
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name
        )
        user_details = UserOrm(
            user=user
        )
        return user, user_details
