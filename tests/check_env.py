# python tests/temp.py
import os
from dotenv import load_dotenv

load_dotenv()

mode = os.getenv("MODE")
print(mode)

google_places_api_key = os.getenv("GOOGLE_PLACES_API_KEY")
print(os.getenv("AZURE_POSTGRES_CONN_STRING"))
print(google_places_api_key)
