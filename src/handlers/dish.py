from fastapi import APIRouter, HTTPException
from typing import List
import uuid

from models import Dish, DishIn
from db.base import database
from db.tables import dishes

router = APIRouter()

@router.get('/{menu_id}/submenus/{sub_id}/dishes', response_model=List[Dish])
async def read_dishes(sub_id: str):
    query = dishes.select().where(dishes.c.sub_menu==sub_id)
    return await database.fetch_all(query)


@router.get('/{menu_id}/submenus/{sub_id}/dishes/{dish_id}', response_model=Dish)
async def read_dish_by_id(sub_id: str, dish_id: str):
    query = dishes.select().where(dishes.c.sub_menu==sub_id, dishes.c.id==dish_id)
    if not (dish := await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail='dish not found')
    return dish      


@router.post('/{menu_id}/submenus/{sub_id}/dishes', response_model=Dish, status_code=201)
async def create_dish(sub_id: str, d: DishIn):
    uid = str(uuid.uuid1())
    query = dishes.insert().values(
        id=uid,
        sub_menu=sub_id,
        title=d.title,
        description=d.description,
        price=d.price
    )
    await database.execute(query)
    return Dish(
        id=uid,
        title=d.title,
        description=d.description,
        price=d.price
    )


@router.patch('/{menu_id}/submenus/{sub_id}/dishes/{dish_id}', response_model=Dish, status_code=200)
async def update_dish(sub_id: str, dish_id: str, d: DishIn):
    query = dishes.update().\
        where(dishes.c.sub_menu==sub_id, dishes.c.id==dish_id).\
        values(
            title=d.title,
            description=d.description,
            price=d.price
        )
    await database.execute(query)

    if not (dish := await read_dish_by_id(sub_id, dish_id)):
        raise HTTPException(status_code=404, detail='dish not found')
    return dish


@router.delete('/{menu_id}/submenus/{sub_id}/dishes/{dish_id}', status_code=200)
async def delete_dish(sub_id: str, dish_id: str):
    query = dishes.delete().where(dishes.c.id==dish_id, dishes.c.sub_menu==sub_id)
    await database.execute(query) 
    return {'status': True, 'message': 'The dish has been deleted'}
