from fastapi import APIRouter, Depends

from db.repository import MenuRepository
from .depends import get_menu_repository


router = APIRouter()

@router.get('/')
async def read_users(
    menu: MenuRepository = Depends(get_menu_repository),
    limit: int = 100, 
    offset: int = 0):
    return {}
