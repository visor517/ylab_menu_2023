from db.base import database
from repositories.menu import MenuRepository


def get_menu_repository() -> MenuRepository:
    return MenuRepository(database)
    