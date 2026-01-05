# from langchain_community.utilities import SQLDatabase

# db = SQLDatabase.from_uri("postgresql://postgres:Hari%401234@localhost:5432/postgres")

# app/db/connection.py - Should look like:
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Hari%401234@localhost:5432/ecommerce_db")
db = create_engine(DATABASE_URL)