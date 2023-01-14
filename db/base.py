from databases import Database
from sqlalchemy import create_engine, MetaData

from config import DATABASE_URL


database = Database(DATABASE_URL + f'?min_size=1&max_size=5')
metadata = MetaData()
engine = create_engine(DATABASE_URL)
