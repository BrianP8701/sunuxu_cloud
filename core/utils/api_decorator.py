import functools
import logging
import traceback
import azure.functions as func
from core.types.api_error import APIError

def api_error_handler(route_handler):
    @functools.wraps(route_handler)
    def wrapper(req: func.HttpRequest) -> func.HttpResponse:
        try:
            return route_handler(req)
        except Exception as e:
            tb = traceback.format_exc()
            error_response = APIError(
                code=500,
                message="An unexpected error occurred.",
                data={"inputs": req.get_json(), "traceback": tb, "error": str(e)},
            )
            logging.error(error_response.model_dump_json())
            return func.HttpResponse(
                body=error_response.model_dump_json(),
                status_code=500,
                mimetype="application/json"
            )
    return wrapper
