# temporary test file to fuck around
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from typing import Optional
from enum import Enum
import os
import json
import azure.functions as func
from api.authentication import signup
from core.database import AzureSQLDatabase
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from pydantic import BaseModel, ConfigDict
from core.models import UserOrm

db = AzureSQLDatabase()
