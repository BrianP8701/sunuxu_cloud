# api/base/add_property/main.py
import azure.functions as func
import json

from core.database import Database
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route(
    route="add_property", methods=["POST"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def add_property(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()

    data = req.get_json()
    property = PropertyOrm(
        user_id=data.get("user_id"),
        street_number=data.get("street_number"),
        street_name=data.get("street_name"),
        street_suffix=data.get("street_suffix"),
        unit=data.get("unit"),
        city=data.get("city"),
        state=data.get("state"),
        zip_code=data.get("zip_code"),
        country=data.get("country"),
        type=data.get("type"),
        status=data.get("status"),
        price=data.get("price"),
        mls_number=data.get("mls_number"),
        bedrooms=data.get("bedrooms"),
        bathrooms=data.get("bathrooms"),
        floors=data.get("floors"),
        rooms=data.get("rooms"),
        kitchens=data.get("kitchens"),
        families=data.get("families"),
        lot_sqft=data.get("lot_sqft"),
        year_built=data.get("year_built"),
        list_start_date=data.get("list_start_date"),
        list_end_date=data.get("list_end_date"),
        expiration_date=data.get("expiration_date"),
        attached_type=data.get("attached_type"),
        section=data.get("section"),
        school_district=data.get("school_district"),
        pictures=data.get("pictures"),
        notes=data.get("notes"),
        description=data.get("description"),
        property_tax=data.get("property_tax"),
    )

    inserted_property = await db.insert(property)

    return func.HttpResponse(
        body=json.dumps({"data": inserted_property.to_dict()}),
        status_code=200,
        mimetype="application/json",
    )
