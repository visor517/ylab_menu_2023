from fastapi import APIRouter, Depends
from typing import List

from db.repository import MenuRepository
from .depends import get_menu_repository
from models import Menu


router = APIRouter()

@router.get('/', response_model=List[Menu])
async def get_menus(
    menus: MenuRepository = Depends(get_menu_repository),
    limit: int = 100, 
    offset: int = 0):
    return await menus.get_all(limit=limit, offset=offset)


# @router.get('/<id>')
# async def get_menu_by_id(
#     menu: MenuRepository = Depends(get_menu_repository),
#     id: int = id):
#     return menu.get_by_id(id=id)


@router.post('/', response_model=Menu, status_code=201)
async def create_menu(
    menu: Menu,
    menus: MenuRepository = Depends(get_menu_repository)):
    return await menus.create(m=menu)
