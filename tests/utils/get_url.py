import os

from dotenv import load_dotenv

load_dotenv()


def get_function_url(func_name: str) -> str:
    mode = os.getenv("MODE")
    if mode in ["local", "dev", "development"]:
        return f"http://localhost:7071/api/{func_name}"
    elif mode == "test":
        azure_function_app = os.getenv("AZURE_FUNCTION_APP_URL")
        host_key = os.getenv("AZURE_FUNCTION_APP_HOST_KEY")
        return f"https://{azure_function_app}.azurewebsites.net/api/{func_name}?code={host_key}"
    else:
        raise ValueError("Invalid mode")
