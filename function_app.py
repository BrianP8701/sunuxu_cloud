# function_app.py
import azure.functions as func 
from api.authentication.login.main import bp as login_bp
from api.authentication.signup.main import bp as signup_bp
from api.admin.delete_user.main import bp as delete_user_bp


app = func.FunctionApp() 

app.register_functions(login_bp)
app.register_functions(signup_bp)
app.register_functions(delete_user_bp)
