# api/google_places/address_autocomplete/main.py
import azure.functions as func
import aiohttp
import os
import json
from dotenv import load_dotenv

from core.models import *
from api.api_utils import api_error_handler

load_dotenv()
blueprint = func.Blueprint()

@blueprint.route(route="get_place_details/{place_id}/{session_token}", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
@api_error_handler
async def get_place_details(req: func.HttpRequest) -> func.HttpResponse:
    place_id = req.route_params.get('place_id')
    session_token = req.route_params.get('session_token')

    key = os.getenv("GOOGLE_PLACES_API_KEY")

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={key}&language=en&fields=address_components&sessiontoken={session_token}"
    response = await aiohttp.ClientSession().get(url)
    response_data = await response.json()

    data = parse_address_components(response_data['result']['address_components'])
    
    return func.HttpResponse(
        body=json.dumps({'data': data}),
        status_code=200,
        mimetype="application/json"
    )

def parse_address_components(address_components):
    parsed_address = {}
    for component in address_components:
        if 'street_number' in component['types']:
            parsed_address['street_number'] = component['long_name']
        elif 'route' in component['types']:
            street_name_parts = component['long_name'].split()
            parsed_address['street_name'] = ' '.join(street_name_parts[:-1])
            parsed_address['street_suffix'] = street_name_parts[-1]
        elif 'locality' in component['types']:
            parsed_address['city'] = component['long_name']
        elif 'administrative_area_level_1' in component['types']:
            parsed_address['state'] = component['short_name']
        elif 'postal_code' in component['types']:
            parsed_address['zip_code'] = component['long_name']
        elif 'country' in component['types']:
            parsed_address['country'] = component['long_name']
    return parsed_address