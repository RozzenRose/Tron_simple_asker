from app.schemas import RemAccount
from app.tron.tron_objects import get_tron_info
from app.functions.db_functions import account_insert, get_select_pages
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all(db: AsyncSession, page: int, limit: int) -> None:
    '''Функция с логикой получения данных'''
    offset = (page - 1) * limit
    return await get_select_pages(db, offset, limit)


async def add_request(db: AsyncSession, address: str) -> dict:
    '''Функция с логикой получения Tron данных и записи в БД'''
    balance, resources = await get_tron_info(address) #Получение данных из Tron
    energy = resources.get('TotalEnergyLimit', 0)
    bandwidth = resources.get('freeNetLimit', 0) + resources.get('TotalNetLimit', 0)

    await account_insert(db, address, balance, energy, bandwidth) #Запись в БД
    return {'account_address': address,
            'balance': balance,
            'energy': energy,
            'bandwidth': bandwidth}