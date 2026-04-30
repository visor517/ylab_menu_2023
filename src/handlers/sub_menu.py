from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from sqlalchemy import select, func

from db.base import AsyncSessionLocal
from db.models import SubMenu, Menu as MenuModel, Dish
from schemas import SubMenuResponse, SubMenuRequest

router = APIRouter()


@router.get('/{menu_id}/submenus', response_model=List[SubMenuResponse], status_code=status.HTTP_200_OK)
async def read_sub_menus(menu_id: str):
    async with AsyncSessionLocal() as session:
        # Проверяем, существует ли меню
        result = await session.execute(
            select(MenuModel).where(MenuModel.id == menu_id)
        )
        menu = result.scalar_one_or_none()
        
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
        
        # Получаем все подменю меню
        result = await session.execute(
            select(SubMenu).where(SubMenu.menu_id == menu_id)
        )
        sub_menus = result.scalars().all()
        
        response = []
        for sub_menu in sub_menus:
            dishes_count = await count_dishes(session, sub_menu.id)
            response.append(SubMenuResponse(
                id=sub_menu.id,
                title=sub_menu.title,
                description=sub_menu.description,
                dishes_count=dishes_count,
            ))
        
        return response


@router.get('/{menu_id}/submenus/{sub_id}', response_model=SubMenuResponse, status_code=status.HTTP_200_OK)
async def read_sub_menu_by_id(menu_id: str, sub_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SubMenu).where(
                SubMenu.id == sub_id,
                SubMenu.menu_id == menu_id
            )
        )
        sub_menu = result.scalar_one_or_none()
        
        if not sub_menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
        
        dishes_count = await count_dishes(session, sub_id)
        
        return SubMenuResponse(
            id=sub_menu.id,
            title=sub_menu.title,
            description=sub_menu.description,
            dishes_count=dishes_count,
        )


@router.post('/{menu_id}/submenus', response_model=SubMenuResponse, status_code=status.HTTP_201_CREATED)
async def create_sub_menu(menu_id: str, m: SubMenuRequest):
    uid = str(uuid.uuid1())
    
    async with AsyncSessionLocal() as session:
        # Проверяем, существует ли меню
        result = await session.execute(
            select(MenuModel).where(MenuModel.id == menu_id)
        )
        menu = result.scalar_one_or_none()
        
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
        
        new_sub_menu = SubMenu(
            id=uid,
            menu_id=menu_id,
            title=m.title,
            description=m.description,
        )
        session.add(new_sub_menu)
        await session.commit()
        
        return SubMenuResponse(
            id=uid,
            title=m.title,
            description=m.description,
            dishes_count=0,
        )


@router.patch('/{menu_id}/submenus/{sub_id}', response_model=SubMenuResponse, status_code=status.HTTP_200_OK)
async def update_sub_menu(menu_id: str, sub_id: str, m: SubMenuRequest):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SubMenu).where(
                SubMenu.id == sub_id,
                SubMenu.menu_id == menu_id
            )
        )
        sub_menu = result.scalar_one_or_none()
        
        if not sub_menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
        
        sub_menu.title = m.title
        sub_menu.description = m.description
        await session.commit()
        
        dishes_count = await count_dishes(session, sub_id)
        
        return SubMenuResponse(
            id=sub_menu.id,
            title=sub_menu.title,
            description=sub_menu.description,
            dishes_count=dishes_count,
        )


@router.delete('/{menu_id}/submenus/{sub_id}', status_code=status.HTTP_200_OK)
async def delete_sub_menu(menu_id: str, sub_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SubMenu).where(
                SubMenu.id == sub_id,
                SubMenu.menu_id == menu_id
            )
        )
        sub_menu = result.scalar_one_or_none()
        
        if not sub_menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')
        
        await session.delete(sub_menu)
        await session.commit()
        
        return {'status': True, 'message': 'The submenu has been deleted'}


async def count_dishes(session, sub_id: str):
    result = await session.execute(
        select(func.count()).select_from(Dish).where(Dish.sub_menu_id == sub_id)
    )
    return result.scalar_one()
