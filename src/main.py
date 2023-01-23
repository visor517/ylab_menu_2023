from fastapi import FastAPI
import uvicorn

from db.base import database
from handlers import menu, sub_menu, dish


app = FastAPI(title='YLAB MENU')

app.include_router(menu.router, prefix='/api/v1/menus', tags=['menus'])
app.include_router(sub_menu.router, prefix='/api/v1/menus', tags=['submenus'])
app.include_router(dish.router, prefix='/api/v1/menus', tags=['dishs'])

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
