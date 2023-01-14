from db.base import database
from db.repository import MenuRepository


def get_menu_repository() -> MenuRepository:
    return MenuRepository(database)
    