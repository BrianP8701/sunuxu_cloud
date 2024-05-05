import os
from dotenv import load_dotenv

load_dotenv()

def get_function_url(func_name: str) -> str:
    mode = os.getenv("MODE")
    if mode == "local" or mode == "test" or mode == "dev" or mode == "development":
        return f"http://localhost:7071/api/{func_name}"
    else:
        return f"{os.getenv('AZURE_FUNCTION_APP_URL')}{func_name}{os.getenv('AZURE_FUNCTION_APP_HOST_KEY')}"
