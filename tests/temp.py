# python tests/temp.py
import os
from dotenv import load_dotenv

load_dotenv()

mode = os.getenv("MODE")
print(mode)  
print(os.getcwd())