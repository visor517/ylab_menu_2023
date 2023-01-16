from pydantic import BaseModel


class Menu(BaseModel):
    id: str
    title: str
    description: str


class MenuIn(BaseModel):
    title: str
    description: str


class SubMenu(BaseModel):
    id: str
    title: str
    description: str


class Dish(BaseModel):
    id: str
    title: str
    description: str
    price: str
