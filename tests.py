import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch

from app.functions.db_functions import account_insert
from app.models import Account
from sqlalchemy import insert
from app.main import app
from app.database.db_depends import get_db
from app.schemas import RemAccount


TEST_ADDRESS = "test_address_123"
MOCK_BALANCE = 1000
MOCK_RESOURCES = {
    "TotalEnergyLimit": 5000,
    "freeNetLimit": 1000,
    "TotalNetLimit": 2000
}

# Мокаем get_db(), чтобы не трогать настоящую БД
@pytest.fixture
def override_get_db():
    async def _override_get_db():
        mock_session = AsyncMock(spec=AsyncSession)
        yield mock_session
    return _override_get_db

@pytest.mark.asyncio
async def test_remember_account(override_get_db):
    # Переопределяем зависимость FastAPI
    app.dependency_overrides[get_db] = override_get_db

    # Мокаем get_tron_info, чтобы не дергать реальный Tron API
    with patch("app.functions.api_functions.get_tron_info") as mock_tron_info:
        mock_tron_info.return_value = (MOCK_BALANCE, MOCK_RESOURCES)

        transport = ASGITransport(app=app, raise_app_exceptions=True)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(f"/account/{TEST_ADDRESS}")

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["account_address"] == TEST_ADDRESS
        assert data["balance"] == MOCK_BALANCE
        assert data["energy"] == MOCK_RESOURCES["TotalEnergyLimit"]
        assert data["bandwidth"] == MOCK_RESOURCES["freeNetLimit"] + MOCK_RESOURCES["TotalNetLimit"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_account_insert_executes_insert_and_commit():
    # 1. Мокаем объект db
    mock_db = AsyncMock()

    # 2. Подготавливаем фиктивную запись
    acc_data = {
        "account_address": "test_address_123",
        "balance": 1000,
        "energy": 5000,
        "bandwidth": 3000
    }

    # 3. Вызываем функцию
    await account_insert(mock_db, acc_data["account_address"],
                         acc_data["balance"],
                         acc_data["energy"],
                         acc_data["bandwidth"])

    expected_acc = RemAccount(**acc_data)
    # 4. Проверяем, что вызван insert с правильными значениями
    expected_stmt = insert(Account).values(**expected_acc.model_dump())
    mock_db.execute.assert_awaited_once()
    mock_db.commit.assert_awaited_once()

    # 5. Проверка аргумента вызова execute
    actual_stmt = mock_db.execute.call_args[0][0]
    assert str(actual_stmt) == str(expected_stmt)  # сравнение SQL-выражений