from fastapi import APIRouter, Depends
from typing import List

from repositories.menu import MenuRepository
from .depends import get_menu_repository
from models import Menu, MenuIn


router = APIRouter()

@router.get('/', response_model=List[Menu])
async def read_menus(
    menus: MenuRepository = Depends(get_menu_repository),
    limit: int = 100, 
    offset: int = 0):
    return await menus.get_all(limit=limit, offset=offset)


@router.get('/{id}', response_model=Menu)
async def read_menu_by_id(
    menus: MenuRepository = Depends(get_menu_repository),
    id: str = id):
    return await menus.get_by_id(id=id)


@router.post('/', response_model=Menu, status_code=201)
async def create_menu(
    menu: MenuIn,
    menus: MenuRepository = Depends(get_menu_repository)):
    return await menus.create(m=menu)


@router.patch('/{id}', response_model=Menu, status_code=200)
async def update_menu(
    menu: MenuIn,
    menus: MenuRepository = Depends(get_menu_repository),
    id: str = id):
    return await menus.update(id=id, m=menu)


@router.delete('/{id}', status_code=200)
async def delete_menu(
    menus: MenuRepository = Depends(get_menu_repository),
    id: str = id):
    return await menus.delete(id=id)
