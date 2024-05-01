from core.database.azure_sql import AzureSQLDatabase

from core.models import *

db = AzureSQLDatabase()

db.delete_tables()
db.create_tables()
