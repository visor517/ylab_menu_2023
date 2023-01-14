from .tables import menus, sub_menus, dishes
from .base import metadata, engine


metadata.create_all(bind=engine)
