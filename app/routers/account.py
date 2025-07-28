from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_depends import get_db
from app.functions.api_functions import get_all, add_request
from fastapi import status, HTTPException


router = APIRouter(prefix='/account', tags=['account'])


@router.get('/all_accounts')
async def all_accounts(db: Annotated[AsyncSession, Depends(get_db)],
                       page: int = 1, limit: int = 5):
    '''Вывод запросов'''
    all_account = await get_all(db, page, limit)
    if all_account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="We don't have any data yet.")
    else:
        return all_account.all()


@router.post('/{address}', status_code=status.HTTP_201_CREATED)
async def remember_account(db: Annotated[AsyncSession, Depends(get_db)], address: str):
    '''Получение данных об аккаунте по адресу с занесением в БД'''
    try:
        return await add_request(db, address)
    except ValueError as e:
        raise HTTPException(status_code=422, detail='Validation failed') from e