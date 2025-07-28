from app.database.engine import session_factory


async def get_db():
    '''Функция для создания сессий'''
    db = session_factory()
    try:
        yield db
    finally:
        await db.close()