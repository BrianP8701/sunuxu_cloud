# python tests/temp.py
import os
from dotenv import load_dotenv

load_dotenv()

mode = os.getenv("MODE")
print(mode)  
print(os.getcwd())

google_places_api_key = os.getenv("GOOGLE_PLACES_API_KEY")
print(google_places_api_key)