import unittest
from dotenv import load_dotenv
import sys
sys.path.append("/Users/brianprzezdziecki/sunuxu/sunuxu")
from core.database.azure_sql import AzureSQLDatabase
from core.models.user import UserOrm, UserTypeEnum
from core.models.todo.participant import ParticipantOrm, ParticipantRoleEnum

load_dotenv()

class AzureSQLDatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):        
        cls.db = AzureSQLDatabase()
        cls.db.create_tables()

    @classmethod
    def tearDownClass(cls):
        cls.db.clear_database("I understand this will delete all data")
        cls.db.Session().close()
        AzureSQLDatabase.reset_instance()

    def test_insert_and_query(self):
        # Create a user
        user = UserOrm(
            username="john_wick",
            password="password",
            email="john@example.com",
            phone=1234567890,
            first_name="John",
            last_name="Doe",
            user_type=UserTypeEnum.PERSON
        )
        self.db.insert(user)

        # Query the user
        users = self.db.query(UserOrm, {"username": "john_wick"})
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, "john_wick")

    def test_update(self):
        # Delete the previously created participant
        self.db.execute_raw_sql("DELETE FROM participants WHERE participant_id = 'P001'")

        # Create a participant
        participant = ParticipantOrm(
            participant_id="P001",
            person_id="1",
            transaction_id="T001",
            role=ParticipantRoleEnum.Buyer,
            relationships="{}"
        )
        self.db.insert(participant)

        # Update the participant
        participant.role = ParticipantRoleEnum.Seller
        self.db.update(participant)

        # Query the updated participant
        participants = self.db.query(ParticipantOrm, {"participant_id": "P001"})
        self.assertEqual(len(participants), 1)
        self.assertEqual(participants[0].role, ParticipantRoleEnum.Seller)

    def test_delete(self):
        # Create a user
        user = UserOrm(
            username="jane_doe",
            password="password",
            email="jane@example.com",
            phone=9876543210,
            first_name="Jane",
            last_name="Doe",
            user_type=UserTypeEnum.AGENT
        )
        self.db.insert(user)

        # Delete the user
        self.db.delete(user)

        # Query the deleted user
        users = self.db.query(UserOrm, {"username": "jane_doe"})
        self.assertEqual(len(users), 0)

    def test_delete_by_id(self):
        # Create a user
        user = UserOrm(
            username="delete_by_id",
            password="password",
            email="delete_by_id@example.com",
            phone="1111111111",
            first_name="Delete",
            last_name="ById",
            user_type=UserTypeEnum.PERSON
        )
        user = self.db.insert(user)  # Use the returned user object

        # Delete the user by ID
        self.db.delete_by_id(user.id, UserOrm)

        # Query the deleted user
        users = self.db.query(UserOrm, {"username": "delete_by_id"})
        self.assertEqual(len(users), 0)

    def test_execute_raw_sql(self):
        # Create multiple participants
        participant1 = ParticipantOrm(
            participant_id="P001",
            person_id="1",
            transaction_id="T001",
            role=ParticipantRoleEnum.Buyer,
            relationships="{}"
        )
        participant2 = ParticipantOrm(
            participant_id="P002",
            person_id="2",
            transaction_id="T001",
            role=ParticipantRoleEnum.Seller,
            relationships="{}"
        )
        self.db.insert(participant1)
        self.db.insert(participant2)

        # Execute raw SQL query
        sql = "SELECT COUNT(*) FROM participants"
        result = self.db.execute_raw_sql(sql)
        self.assertEqual(result[0][0], 2)

    def test_transactions(self):
        # Define the operations to perform within the transaction
        def operations(session):
            user = UserOrm(
                username="alice",
                password="password",
                email="alice@example.com",
                phone=1111111111,
                first_name="Alice",
                last_name="Smith",
                user_type=UserTypeEnum.PERSON
            )
            session.add(user)

        # Perform the transaction
        self.db.perform_transaction(operations)

        # Query the user after the transaction
        users = self.db.query(UserOrm, {"username": "alice"})
        self.assertEqual(len(users), 1)

if __name__ == "__main__":
    unittest.main()
