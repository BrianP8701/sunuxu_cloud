# api/test_2.py
import azure.functions as func 
import logging

bp = func.Blueprint()

@bp.route(route="test_2", auth_level=func.HttpAuthLevel.FUNCTION)
@bp.function_name(name="test_2")
async def test_2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get('name')

    if not name:
        raise Exception("Name is required.")

    return {"message": f"Hello, {name}. This HTTP triggered function executed successfully."}

