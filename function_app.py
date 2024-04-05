# function_app.py
import azure.functions as func 
from api import *

app = func.FunctionApp() 

app.register_functions(authentication_bp)
app.register_functions(admin_bp)