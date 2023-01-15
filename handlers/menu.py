from fastapi import APIRouter, Depends

from db.repository import MenuRepository
from .depends import get_menu_repository


router = APIRouter()

@router.get('/')
async def get_menus(
    menu: MenuRepository = Depends(get_menu_repository),
    limit: int = 100, 
    offset: int = 0):
    return menu.get_all(limit=limit, offset=offset)


@router.get('/<id>')
async def get_menu_by_id(
    menu: MenuRepository = Depends(get_menu_repository),
    id: int = id):
    return menu.get_by_id(id=id)
