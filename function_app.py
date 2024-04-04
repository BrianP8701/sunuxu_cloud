# function_app.py
import azure.functions as func 
from api import *

app = func.FunctionApp() 

app.register_functions(test_1_bp)
app.register_functions(test_2_bp)