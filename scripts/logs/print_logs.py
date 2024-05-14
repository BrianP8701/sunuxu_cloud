from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus

load_dotenv()


def fetch_function_app_logs(app_name, time_period):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    workspace_id = os.getenv("AZURE_LOG_WORKSPACE_ID")

    # Parse the time period
    num, unit = time_period.split()
    num = int(num)

    now = datetime.utcnow()
    if unit == "minutes":
        time_ago = now - timedelta(minutes=num)
    elif unit == "hours":
        time_ago = now - timedelta(hours=num)
    else:
        raise ValueError(
            "Time period should be in the format '<number> minutes' or '<number> hours'"
        )

    kql_query = f"""
    traces
    | where timestamp > datetime({time_ago.isoformat()}Z) and timestamp <= datetime({now.isoformat()}Z)
    | where cloud_RoleName == '{app_name}'
    | project timestamp, message, severityLevel
    | order by timestamp desc
    | limit 100
    """

    try:
        response = client.query_workspace(
            workspace_id, kql_query, timespan=(time_ago, now)
        )
        if response.status == LogsQueryStatus.SUCCESS:
            for log in response.tables[0].rows:
                print(f"Timestamp: {log[0]}, Message: {log[1]}, Severity: {log[2]}")
        else:
            print("Failed to fetch logs")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage: Fetch logs for the past 5 minutes
fetch_function_app_logs("sunuxu-test-functions", "5 minutes")
