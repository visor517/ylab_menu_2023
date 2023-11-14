from databases import Database
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, MetaData

load_dotenv()
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'


database = Database(DATABASE_URL + f'?min_size=1&max_size=5')
metadata = MetaData()
engine = create_engine(DATABASE_URL)
