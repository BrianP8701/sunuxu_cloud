# function_app.py
import azure.functions as func 
from login import bp as login_bp
from signup import bp as signup_bp
from delete_user import bp as delete_user_bp


app = func.FunctionApp() 

app.register_functions(login_bp)
app.register_functions(signup_bp)
app.register_functions(delete_user_bp)
