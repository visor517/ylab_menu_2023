from fastapi import APIRouter, HTTPException
from typing import List
import uuid

from models import SubMenu, SubMenuIn
from db.base import database
from db.tables import sub_menus, dishes

router = APIRouter()

@router.get('/{menu_id}/submenus', response_model=List[SubMenu])
async def read_sub_menus(menu_id: str):
    query = sub_menus.select().where(sub_menus.c.menu==menu_id)
    return await database.fetch_all(query)


@router.get('/{menu_id}/submenus/{sub_id}', response_model=SubMenu)
async def read_sub_menu_by_id(menu_id: str, sub_id: str):
    query = sub_menus.select().where(sub_menus.c.menu==menu_id, sub_menus.c.id==sub_id)
    if not (sub_menu := await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail='submenu not found')
    
    count = await count_dishes(sub_id)
    return SubMenu(**sub_menu, dishes_count=count)     


@router.post('/{menu_id}/submenus', response_model=SubMenu, status_code=201)
async def create_sub_menu(menu_id: str, m: SubMenuIn):
    uid = str(uuid.uuid1())
    query = sub_menus.insert().values(
        id=uid,
        menu=menu_id,
        title=m.title,
        description=m.description,
    )
    await database.execute(query)
    return SubMenu(
        id=uid,
        title=m.title,
        description=m.description
    )


@router.patch('/{menu_id}/submenus/{sub_id}', response_model=SubMenu, status_code=200)
async def update_sub_menu(menu_id: str, sub_id: str, m: SubMenuIn):
    query = sub_menus.update().\
        where(sub_menus.c.id==sub_id, sub_menus.c.menu==menu_id).\
        values(
            title=m.title,
            description=m.description,
        )
    await database.execute(query)

    if not (sub_menu := await read_sub_menu_by_id(menu_id, sub_id)):
        raise HTTPException(status_code=404, detail='submenu not found')
    return sub_menu


@router.delete('/{menu_id}/submenus/{sub_id}', status_code=200)
async def delete_sub_menu(menu_id: str, sub_id: str):
    query = sub_menus.delete().where(sub_menus.c.id==sub_id, sub_menus.c.menu==menu_id)
    await database.execute(query) 
    return {'status': True, 'message': 'The submenu has been deleted'}


async def count_dishes(sub_id: str):
    query = dishes.select().where(dishes.c.sub_menu==sub_id)
    dish = await database.fetch_all(query)
    return len(dish)
