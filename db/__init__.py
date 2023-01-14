from .models import menus, sub_menus, dishes
from .base import metadata, engine


metadata.create_all(bind=engine)
