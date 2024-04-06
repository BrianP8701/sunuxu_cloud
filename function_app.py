# function_app.py
import azure.functions as func 

from api.authentication import blueprint as authentication_bp
from api.admin import blueprint as admin_bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

app.register_functions(authentication_bp)
app.register_functions(admin_bp)


