from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from sqlalchemy import select, func

from db.base import AsyncSessionLocal
from db.models import Menu, SubMenu, Dish
from schemas import MenuResponse, MenuRequest

router = APIRouter()


@router.get('/', response_model=List[MenuResponse])
async def read_menus():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Menu))
        menus = result.scalars().all()
        
        response = []
        for menu in menus:
            submenus_count, dishes_count = await count_extra_params(session, menu.id)
            response.append(MenuResponse(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=submenus_count,
                dishes_count=dishes_count,
            ))
        
        return response


@router.get('/{menu_id}', response_model=MenuResponse)
async def read_menu_by_id(menu_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Menu).where(Menu.id == menu_id)
        )
        menu = result.scalar_one_or_none()
        
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
        
        submenus_count, dishes_count = await count_extra_params(session, menu_id)
        
        return MenuResponse(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count,
        )


@router.post('/', response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(m: MenuRequest):
    uid = str(uuid.uuid1())
    
    async with AsyncSessionLocal() as session:
        new_menu = Menu(
            id=uid,
            title=m.title,
            description=m.description,
        )
        session.add(new_menu)
        await session.commit()
        
        return MenuResponse(
            id=uid,
            title=m.title,
            description=m.description,
            submenus_count=0,
            dishes_count=0,
        )


@router.patch('/{menu_id}', response_model=MenuResponse, status_code=status.HTTP_200_OK)
async def update_menu(menu_id: str, m: MenuRequest):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Menu).where(Menu.id == menu_id)
        )
        menu = result.scalar_one_or_none()
        
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
        
        menu.title = m.title
        menu.description = m.description
        await session.commit()
        
        submenus_count, dishes_count = await count_extra_params(session, menu_id)
        
        return MenuResponse(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count,
        )


@router.delete('/{menu_id}', status_code=status.HTTP_200_OK)
async def delete_menu(menu_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Menu).where(Menu.id == menu_id)
        )
        menu = result.scalar_one_or_none()
        
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
        
        await session.delete(menu)
        await session.commit()
        
        return {'status': True, 'message': 'The menu has been deleted'}


async def count_extra_params(session, menu_id: str):
    # Подсчет подменю
    result = await session.execute(
        select(func.count()).select_from(SubMenu).where(SubMenu.menu_id == menu_id)
    )
    submenus_count = result.scalar_one()
    
    # Подсчет блюд через подменю
    result = await session.execute(
        select(func.count()).select_from(Dish).join(SubMenu).where(SubMenu.menu_id == menu_id)
    )
    dishes_count = result.scalar_one()
    
    return (submenus_count, dishes_count)
