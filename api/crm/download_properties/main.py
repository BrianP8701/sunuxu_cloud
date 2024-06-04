# api/crm/download_properties/main.py
import azure.functions as func
import pandas as pd
from io import BytesIO

from core.database import Database
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route("download_properties", methods=["POST"])
@api_error_handler
async def download_properties(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()

    data = req.get_json()

    property_ids = data.get("transaction_ids")
    columns = data.get("columns")

    properties = await db.batch_query(
        PropertyOrm, conditions={"id": property_ids}, columns=columns
    )

    # Check the structure of 'properties' and convert accordingly
    if properties:
        # If 'properties' is a list of tuples, convert it to a list of dicts
        if isinstance(properties[0], tuple):
            properties = [dict(zip(columns, t)) for t in properties]
        df = pd.DataFrame(properties, columns=columns)
    else:
        df = pd.DataFrame(columns=columns)

    # Create an Excel writer object and convert the DataFrame to an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Properties")

    # Get the Excel file content
    excel_data = output.getvalue()

    # Set the response with the Excel file
    return func.HttpResponse(
        body=excel_data,
        status_code=200,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="download_properties.xlsx"'
        },
    )
