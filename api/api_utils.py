import functools
import logging
import traceback

import azure.functions as func

from core.objects.api_error import APIError


def api_error_handler(route_handler):
    @functools.wraps(route_handler)
    async def wrapper(req: func.HttpRequest) -> func.HttpResponse:
        try:
            return await route_handler(req)
        except Exception as e:
            tb = traceback.format_exc()
            try:
                inputs = req.get_json()
            except ValueError:
                inputs = {}
            return return_server_error(
                f"An unexpected error occurred: {str(e)}",
                data={"inputs": inputs, "traceback": tb, "error": str(e)},
            )

    return wrapper


def parse_request_body(req):
    try:
        req_body = req.get_json()
        return req_body
    except ValueError:
        raise ValueError("Request body is not valid JSON")


def return_server_error(message: str, status_code: int = 500, data: dict = {}):
    error_response = APIError(code=status_code, message=message, data=data)

    if status_code == 500:
        logging.error(error_response.model_dump_json())

    return func.HttpResponse(
        body=error_response.model_dump_json(),
        status_code=status_code,
        mimetype="application/json",
    )
