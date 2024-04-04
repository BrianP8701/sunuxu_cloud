import os
import unittest
import time
import sys
sys.path.append("/Users/brianprzezdziecki/sunuxu/sunuxu")
from sunuxu.database.sqlite import AzureSqlDatabase
from sunuxu.models.user import UserOrm, UserTypeEnum
from sunuxu.models.participant import ParticipantOrm, ParticipantRoleEnum

class SQLiteDatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.db_file = "/Users/brianprzezdziecki/sunuxu/sunuxu/tests/sqlite_test_db.sqlite3"
        with open(self.db_file, 'w') as db:
            pass
        self.db = AzureSqlDatabase.get_instance(self.db_file)
        self.db.create_tables()

    def tearDown(self):
        self.db.Session().close()
        os.remove(self.db_file)
        AzureSqlDatabase.reset_instance()

    def test_insert_and_query(self):
        # Create a user
        user = UserOrm(
            username="john_doe",
            password="password",
            email="john@example.com",
            phone=1234567890,
            first_name="John",
            last_name="Doe",
            user_type=UserTypeEnum.PERSON
        )
        self.db.insert(user)

        # Query the user
        users = self.db.query(UserOrm, {"username": "john_doe"})
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, "john_doe")

    def test_update(self):
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
            session.add(user)  # Directly use session.add here

        # Perform the transaction
        self.db.perform_transaction(operations)

        # Query the user after the transaction
        users = self.db.query(UserOrm, {"username": "alice"})
        self.assertEqual(len(users), 1)


if __name__ == "__main__":
    unittest.main()
