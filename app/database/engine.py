from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.database.db_config import settings

#создаем асинхронный движек
engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True)
#создаем асинхронную фабрику сессий
session_factory = async_sessionmaker(engine)

#объявляем класс для моделей
class Base(DeclarativeBase):
    pass