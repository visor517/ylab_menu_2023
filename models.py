from pydantic import BaseModel
from typing import Optional


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
    dishes_count: int = 0


class SubMenuIn(BaseModel):
    title: str
    description: str


class Dish(BaseModel):
    id: str
    title: str
    description: str
    price: str


class DishIn(BaseModel):
    title: str
    description: str
    price: str
