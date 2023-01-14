from fastapi import FastAPI
import uvicorn

from db.base import database
from handlers import menu


app = FastAPI(title='YLAB MENU')
app.include_router(menu.router, prefix='/api/v1/menus', tags=['menus'])

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
