from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = 'postgresql://fastapi:fastapi@db/menu'


database = Database(DATABASE_URL + f'?min_size=1&max_size=5')
metadata = MetaData()
engine = create_engine(DATABASE_URL)
