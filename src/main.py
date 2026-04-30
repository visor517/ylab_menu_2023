from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from db.base import database, engine
from db.tables import metadata
from handlers import menu, sub_menu, dish


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем таблицы в базе данных при старте сервера
    metadata.create_all(engine)
    await database.connect()
    print('Database connected')
    yield
    await database.disconnect()
    print('Database disconnected')

app = FastAPI(title='MENU', lifespan=lifespan)

app.include_router(menu.router, prefix='/api/v1/menus', tags=['menus'])
app.include_router(sub_menu.router, prefix='/api/v1/menus', tags=['submenus'])
app.include_router(dish.router, prefix='/api/v1/menus', tags=['dishs'])
