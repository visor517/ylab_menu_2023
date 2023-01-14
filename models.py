from typing import Optional
from pydantic import BaseModel


class Menu(BaseModel):
    id: Optional[str] = None
    title: str
    description: str


class SubMenu(BaseModel):
    id: Optional[str] = None
    title: str
    description: str


class Dish(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    price: str
