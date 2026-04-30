from pydantic import BaseModel


# Request модели (для входящих данных)
class MenuRequest(BaseModel):
    title: str
    description: str


class SubMenuRequest(BaseModel):
    title: str
    description: str


class DishRequest(BaseModel):
    title: str
    description: str
    price: str


# Response модели (для исходящих данных)
class MenuResponse(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0


class SubMenuResponse(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int = 0


class DishResponse(BaseModel):
    id: str
    title: str
    description: str
    price: str
