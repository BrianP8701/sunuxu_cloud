import unittest
from dotenv import load_dotenv

from core.database.azure_sql import AzureSQLDatabase
from core.models.users import UserOrm
from core.models.todo.participant import ParticipantOrm, ParticipantRoleEnum

load_dotenv()

class AzureSQLDatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):        
        cls.db = AzureSQLDatabase()

    @classmethod
    def tearDownClass(cls):
        cls.db.clear_database("I understand this will delete all data")
        AzureSQLDatabase.dispose_instance()

    def test_insert_and_query(self):
        # Create a user
        user = UserOrm(
            email="john@example.com",
            password="password",
            phone="1234567890",
            first_name="John",
            middle_name="",
            last_name="Doe",
            user_type="person"
        )
        self.db.insert(user)

        # Query the user
        users = self.db.query(UserOrm, {"email": "john@example.com"})
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, "john@example.com")

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
            email="jane@example.com",
            password="password",
            phone="9876543210",
            first_name="Jane",
            middle_name="",
            last_name="Doe",
            user_type="agent"
        )
        self.db.insert(user)

        # Delete the user
        self.db.delete(UserOrm, {"email": "jane@example.com"})

        # Query the deleted user
        users = self.db.query(UserOrm, {"email": "jane@example.com"})
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
                email="alice@example.com",
                password="password",
                phone="1111111111",
                first_name="Alice",
                middle_name="",
                last_name="Smith",
                user_type="person"
            )
            session.add(user)

        # Perform the transaction
        self.db.perform_transaction(operations)

        # Query the user after the transaction
        users = self.db.query(UserOrm, {"email": "alice@example.com"})
        self.assertEqual(len(users), 1)

    def test_exists(self):
        # Create a user
        user = UserOrm(
            email="test_exists@example.com",
            password="password",
            phone="1234567890",
            first_name="Test",
            middle_name="",
            last_name="Exists",
            user_type="person"
        )
        self.db.insert(user)

        # Check if the user exists
        exists = self.db.exists(UserOrm, {"email": "test_exists@example.com"})
        self.assertTrue(exists)

        # Check if a non-existing user exists
        not_exists = self.db.exists(UserOrm, {"email": "non_existing_user@example.com"})
        self.assertFalse(not_exists)

if __name__ == "__main__":
    unittest.main()
