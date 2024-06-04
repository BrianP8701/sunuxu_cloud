# api/crm/download_people/main.py
import azure.functions as func
import pandas as pd
from io import BytesIO

from core.database import Database
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route("download_people", methods=["POST"])
@api_error_handler
async def download_people(req: func.HttpRequest) -> func.HttpResponse:
    db = Database()

    data = req.get_json()

    people_ids = data.get("people_ids")
    columns = data.get("columns")

    people = await db.batch_query(
        PersonOrm, conditions={"id": people_ids}, columns=columns
    )

    print(people)
    print(type(people))

    # Check the structure of 'people' and convert accordingly
    if people:
        # If 'people' is a list of tuples, convert it to a list of dicts
        if isinstance(people[0], tuple):
            people = [dict(zip(columns, p)) for p in people]
        df = pd.DataFrame(people, columns=columns)
    else:
        df = pd.DataFrame(columns=columns)

    # Create an Excel writer object and convert the DataFrame to an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="People")

    # Get the Excel file content
    excel_data = output.getvalue()

    # Set the response with the Excel file
    return func.HttpResponse(
        body=excel_data,
        status_code=200,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="download_people.xlsx"'},
    )
