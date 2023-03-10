from fastapi import APIRouter, HTTPException
from typing import List
import uuid

from models import Menu, MenuIn, SubMenu
from db.base import database
from db.tables import menus, sub_menus, dishes
from sqlalchemy.sql.expression import func, select


router = APIRouter()

@router.get('/', response_model=List[Menu])
async def read_menus():
    query = menus.select()
    return await database.fetch_all(query)


@router.get('/{menu_id}', response_model=Menu)
async def read_menu_by_id(menu_id: str):
    query = menus.select().where(menus.c.id==menu_id)
    if not (menu := await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail='menu not found')

    submenus_count, dishes_count = await count_extra_params(menu_id)
    return Menu(
        **menu,
        submenus_count=submenus_count,
        dishes_count=dishes_count,
    )


@router.post('/', response_model=Menu, status_code=201)
async def create_menu(m: MenuIn):
    uid = str(uuid.uuid1())
    query = menus.insert().values(
        id=uid,
        title=m.title,
        description=m.description,
    )
    await database.execute(query)
    return Menu(
        id=uid,
        title=m.title,
        description=m.description
    )


@router.patch('/{menu_id}', response_model=Menu, status_code=200)
async def update_sub_menu(menu_id: str, m: MenuIn):
    query = menus.update().\
        where(menus.c.id==menu_id).\
        values(
            title=m.title,
            description=m.description,
        )
    await database.execute(query)

    if not (menu := await read_menu_by_id(menu_id)):
        raise HTTPException(status_code=404, detail='menu not found')
    return menu


@router.delete('/{menu_id}', status_code=200)
async def delete_sub_menu(menu_id: str):
    query = menus.delete().where(menus.c.id==menu_id)
    await database.execute(query) 
    return {'status': True, 'message': 'The menu has been deleted'}


async def count_extra_params(menu_id: str):
    query = sub_menus.select().where(sub_menus.c.menu==menu_id)
    sub_menu_list = await database.fetch_all(query)
    dishes_count = 0
    print(sub_menu_list)
    for sub in sub_menu_list:
        sub_id = sub['id']
        query = dishes.select().where(dishes.c.sub_menu==sub_id)
        dishes_list = await database.fetch_all(query)
        dishes_count += len(dishes_list)

    return (len(sub_menu_list), dishes_count)
