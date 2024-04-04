from sunuxu.database.azure_sql import AzureSQLDatabase
from sunuxu.models import *

db = AzureSQLDatabase()
# db.create_tables()        If i dont run this line it nothing happens, like the table doesent exist.
db.clear_database("I understand this will delete all data")