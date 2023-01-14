from typing import List, Optional

from databases import Database

from db.tables import menus, sub_menus, dishes
from models import Menu, SubMenu, Dish


class BaseRepository:
    def __init__(self, database: Database):
        self.database = database


class MenuRepository(BaseRepository):
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Menu]:
        query = menus.select().limit(limit).offset(offset)
        return await self.database.fetch_all(query)

    async def get_by_id(self, id: int) -> Optional[Menu]:
        query = menus.select().where(menus.c.id==id)
        if menu := await self.database.fetch_one(query):
            return Menu.parse_obj(menu)

    async def create(self, m):
        menu = Menu(
            title=m.title,
            description=m.description,
        )
        values = {**menu.dict()}
        values.pop('id', None)
        query = menus.insert().values(**values)
        menu.id = await self.database.execute(query)
        return menu

    async def update(self, id: int, m):
        menu = Menu(
            id=id,
            title=m.title,
            description=m.description,
        )
        values = {**menu.dict()}
        values.pop('id', None)
        query = menus.update().where(menus.c.id==id).values(**values)
        await self.database.execute(query)
        return menu

    async def delete():
        pass
