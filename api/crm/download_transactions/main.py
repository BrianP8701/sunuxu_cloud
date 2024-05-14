# api/crm/download_transactions/main.py
import azure.functions as func
import pandas as pd
from io import BytesIO
from typing import List

from core.database import AzurePostgreSQLDatabase
from core.models import *
from api.api_utils import api_error_handler

blueprint = func.Blueprint()


@blueprint.route("download_transactions", methods=["POST"])
@api_error_handler
async def download_transactions(req: func.HttpRequest) -> func.HttpResponse:
    db = AzurePostgreSQLDatabase()

    data = req.get_json()

    transaction_ids = data.get("transaction_ids")
    columns = data.get("columns")

    transactions = await db.batch_query(
        TransactionOrm, conditions={"id": transaction_ids}, columns=columns
    )

    # Check the structure of 'transactions' and convert accordingly
    if transactions:
        # If 'transactions' is a list of tuples, convert it to a list of dicts
        if isinstance(transactions[0], tuple):
            transactions = [dict(zip(columns, t)) for t in transactions]
        df = pd.DataFrame(transactions, columns=columns)
    else:
        df = pd.DataFrame(columns=columns)

    # Create an Excel writer object and convert the DataFrame to an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Transactions")

    # Get the Excel file content
    excel_data = output.getvalue()

    # Set the response with the Excel file
    return func.HttpResponse(
        body=excel_data,
        status_code=200,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="download_transactions.xlsx"'
        },
    )
