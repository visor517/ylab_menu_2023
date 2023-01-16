from .tables import menus, sub_menus, dishes
from db.base import metadata, engine

# сбрасываем
metadata.drop_all(bind=engine)

# создаем таблицы
metadata.create_all(bind=engine)
