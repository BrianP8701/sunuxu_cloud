# api/test_1.py
import azure.functions as func
import logging
from dotenv import load_dotenv
from sunuxu.database import AzureSQLDatabase
from sunuxu.models import UserOrm, UserTypeEnum
from sunuxu.models import *

load_dotenv()
db = AzureSQLDatabase()

bp = func.Blueprint()

@bp.route(route="test_1", auth_level=func.HttpAuthLevel.FUNCTION)
@bp.function_name(name="test_1")
def test_1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    db.insert(UserOrm(
            id=10,
            username=name,
            password="password",
            email="john@example.com",
            phone=1234567890,
            first_name="John",
            middle_name="Doe",
            last_name="Doe",
            user_type=UserTypeEnum.ADMIN
    ))
    
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
