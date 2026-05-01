from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.base import engine
from db.models import Base
from handlers import menu, sub_menu, dish


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем таблицы в базе данных при старте сервера
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database connected")
    yield
    await engine.dispose()
    print("Database disconnected")


app = FastAPI(title="MENU", lifespan=lifespan)

app.include_router(menu.router, prefix="/api/v1/menus", tags=["menus"])
app.include_router(sub_menu.router, prefix="/api/v1/menus", tags=["submenus"])
app.include_router(dish.router, prefix="/api/v1/menus", tags=["dishes"])
