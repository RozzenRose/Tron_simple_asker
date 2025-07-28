from sqlalchemy import insert, select
from app.models.account import Account
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import RemAccount


async def get_select_pages(db: AsyncSession, offset: int, limit: int):
    '''Запрос данных из БД с пагинацией'''
    return await db.scalars(select(Account).order_by(Account.id.desc()).offset(offset).limit(limit))



async def account_insert(db: AsyncSession, address: str, balance: float, energy: int, bandwidth: int):
    '''Запись данных в базу данных'''
    create_acc = RemAccount(account_address=address,
                            balance=balance,
                            energy=energy,
                            bandwidth=bandwidth)
    insert_data = insert(Account).values(**create_acc.model_dump())
    await db.execute(insert_data)
    await db.commit()