from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from sqlalchemy import select

from db.base import AsyncSessionLocal
from db.models import Dish, SubMenu
from schemas import DishResponse, DishRequest

router = APIRouter()


@router.get('/{menu_id}/submenus/{sub_id}/dishes', response_model=List[DishResponse], status_code=status.HTTP_200_OK)
async def read_dishes(menu_id: str, sub_id: str):
    async with AsyncSessionLocal() as session:
        # Проверяем, существует ли подменю
        result = await session.execute(
            select(SubMenu).where(SubMenu.id == sub_id, SubMenu.menu_id == menu_id)
        )
        submenu = result.scalar_one_or_none()
        
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
        
        # Получаем все блюда подменю
        result = await session.execute(
            select(Dish).where(Dish.sub_menu_id == sub_id)
        )
        dishes = result.scalars().all()
        
        return [
            DishResponse(
                id=dish.id,
                title=dish.title,
                description=dish.description,
                price=dish.price
            )
            for dish in dishes
        ]


@router.get('/{menu_id}/submenus/{sub_id}/dishes/{dish_id}', response_model=DishResponse, status_code=status.HTTP_200_OK)
async def read_dish_by_id(menu_id: str, sub_id: str, dish_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Dish).where(
                Dish.id == dish_id,
                Dish.sub_menu_id == sub_id
            )
        )
        dish = result.scalar_one_or_none()
        
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
        
        return DishResponse(
            id=dish.id,
            title=dish.title,
            description=dish.description,
            price=dish.price
        )


@router.post('/{menu_id}/submenus/{sub_id}/dishes', response_model=DishResponse, status_code=status.HTTP_201_CREATED)
async def create_dish(menu_id: str, sub_id: str, d: DishRequest):
    uid = str(uuid.uuid1())
    
    async with AsyncSessionLocal() as session:
        # Проверяем, существует ли подменю
        result = await session.execute(
            select(SubMenu).where(SubMenu.id == sub_id, SubMenu.menu_id == menu_id)
        )
        submenu = result.scalar_one_or_none()
        
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
        
        new_dish = Dish(
            id=uid,
            sub_menu_id=sub_id,
            title=d.title,
            description=d.description,
            price=d.price
        )
        session.add(new_dish)
        await session.commit()
        
        return DishResponse(
            id=uid,
            title=d.title,
            description=d.description,
            price=d.price
        )


@router.patch('/{menu_id}/submenus/{sub_id}/dishes/{dish_id}', response_model=DishResponse, status_code=status.HTTP_200_OK)
async def update_dish(menu_id: str, sub_id: str, dish_id: str, d: DishRequest):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Dish).where(
                Dish.id == dish_id,
                Dish.sub_menu_id == sub_id
            )
        )
        dish = result.scalar_one_or_none()
        
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
        
        dish.title = d.title
        dish.description = d.description
        dish.price = d.price
        await session.commit()
        
        return DishResponse(
            id=dish.id,
            title=dish.title,
            description=dish.description,
            price=dish.price
        )


@router.delete('/{menu_id}/submenus/{sub_id}/dishes/{dish_id}', status_code=status.HTTP_200_OK)
async def delete_dish(menu_id: str, sub_id: str, dish_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Dish).where(
                Dish.id == dish_id,
                Dish.sub_menu_id == sub_id
            )
        )
        dish = result.scalar_one_or_none()
        
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
        
        await session.delete(dish)
        await session.commit()
        
        return {'status': True, 'message': 'The dish has been deleted'}
