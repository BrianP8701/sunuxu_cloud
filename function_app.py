# function_app.py
import azure.functions as func
from dotenv import load_dotenv

from api import get_blueprints
from core.models import *

load_dotenv()

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Load all blueprints dynamically
blueprints = get_blueprints()
for blueprint in blueprints:
    print(blueprint)
    app.register_blueprint(blueprint)
