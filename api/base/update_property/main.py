# api/base/update_property/main.py
import azure.functions as func

from api.api_utils import api_error_handler
from core.database import Database
from core.models import *

blueprint = func.Blueprint()


@blueprint.route(
    route="update_property", methods=["PUT"], auth_level=func.AuthLevel.FUNCTION
)
@api_error_handler
async def update_property(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()

    data = req.get_json()

    property = PropertyModel(
        id=data.get("id"),
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

    await db.update(property)

    return func.HttpResponse(status_code=200, mimetype="application/json")
