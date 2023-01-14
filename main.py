from fastapi import FastAPI
import uvicorn

from db.base import database


app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
