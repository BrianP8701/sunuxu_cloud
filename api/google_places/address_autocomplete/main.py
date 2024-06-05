# api/google_places/address_autocomplete/main.py
import json
import os

import aiohttp
import azure.functions as func
from dotenv import load_dotenv

from api.api_utils import api_error_handler
from core.models import *

load_dotenv()
blueprint = func.Blueprint()


@blueprint.route(
    route="address_autocomplete/{query}/{session_token}",
    methods=["GET"],
    auth_level=func.AuthLevel.FUNCTION,
)
@api_error_handler
async def address_autocomplete(req: func.HttpRequest) -> func.HttpResponse:
    query = req.route_params.get("query")
    session_token = req.route_params.get("session_token")

    key = os.getenv("GOOGLE_PLACES_API_KEY")

    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={query}&key={key}&language=en&sessiontoken={session_token}"
    response = await aiohttp.ClientSession().get(url)
    response_data = await response.json()

    data = []
    for prediction in response_data["predictions"]:
        data.append(
            {"place_id": prediction["place_id"], "address": prediction["description"]}
        )

    return func.HttpResponse(
        body=json.dumps({"data": data}), status_code=200, mimetype="application/json"
    )
