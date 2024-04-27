import os

def get_function_url(route: str):
    return f"{os.getenv('AZURE_FUNCTION_APP_URL')}{route}{os.getenv('AZURE_FUNCTION_APP_HOST_KEY')}"
