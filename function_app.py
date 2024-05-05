# function_app.py
import azure.functions as func 
from dotenv import load_dotenv

from api.authentication.authenticate_token.main import blueprint as authentication_bp
from api.authentication.refresh_token.main import blueprint as refresh_token_bp
from api.authentication.signin.main import blueprint as signin_bp
from api.authentication.signup.main import blueprint as signup_bp

from api.admin.delete_user.main import blueprint as delete_user_bp
from api.base.get_person.main import blueprint as get_person_bp
from api.base.get_property.main import blueprint as get_property_bp
from api.base.get_transaction.main import blueprint as get_transaction_bp
from api.base.delete_person.main import blueprint as delete_person_bp
from api.base.delete_property.main import blueprint as delete_property_bp
from api.base.delete_transaction.main import blueprint as delete_transaction_bp
from api.base.add_person.main import blueprint as add_person_bp
from api.base.add_property.main import blueprint as add_property_bp
from api.base.add_transaction.main import blueprint as add_transaction_bp
from api.base.update_person.main import blueprint as update_person_bp
from api.base.update_property.main import blueprint as update_property_bp
from api.base.update_transaction.main import blueprint as update_transaction_bp

from api.crm.get_table_data.main import blueprint as get_table_data_bp
from api.crm.download_people.main import blueprint as download_people_bp

from core.models import *

load_dotenv()

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

app.register_functions(signin_bp)
app.register_functions(signup_bp)
app.register_functions(authentication_bp)
app.register_functions(refresh_token_bp)
app.register_functions(delete_user_bp)
app.register_functions(get_table_data_bp)
app.register_functions(get_property_bp)
app.register_functions(get_person_bp)
app.register_functions(get_transaction_bp)
app.register_functions(delete_person_bp)
app.register_functions(delete_property_bp)
app.register_functions(delete_transaction_bp)
app.register_functions(add_person_bp)
app.register_functions(add_property_bp)
app.register_functions(add_transaction_bp)
app.register_functions(update_person_bp)
app.register_functions(update_property_bp)
app.register_functions(update_transaction_bp)
app.register_functions(download_people_bp)
