from typing import List, Optional
import uuid


from repositories.base import BaseRepository
from db.tables import menus
from models import Menu, MenuIn


class MenuRepository(BaseRepository):
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Menu]:
        query = menus.select().limit(limit).offset(offset)
        return await self.database.fetch_all(query)

    async def get_by_id(self, id: str) -> Optional[Menu]:
        query = menus.select().where(menus.c.id==id)
        if menu := await self.database.fetch_one(query):
            return Menu.parse_obj(menu)
        return None

    async def create(self, m: MenuIn):
        menu = Menu(
            id=str(uuid.uuid1()),
            title=m.title,
            description=m.description,
        )
        values = {**menu.dict()}
        query = menus.insert().values(**values)
        await self.database.execute(query)
        return menu

    async def update(self, id: str, m: MenuIn):
        menu = Menu(
            id=id,
            title=m.title,
            description=m.description,
        )
        values = {**menu.dict()}
        query = menus.update().where(menus.c.id==id).values(**values)
        await self.database.execute(query)
        return menu

    async def delete(self, id: str):
        query = menus.delete().where(menus.c.id==id)
        await self.database.execute(query)
