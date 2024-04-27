from core.database.azure_sql import AzureSQLDatabase

from core.models.accounts import AccountOrm
from core.models.users import UserOrm

db = AzureSQLDatabase()

db.delete_tables()
db.create_tables()
