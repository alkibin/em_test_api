import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from asgi_lifespan import LifespanManager

from init_db import init_db, fill_bd_test_data, drop_db
from main import app


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client(event_loop):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client


@pytest_asyncio.fixture(scope='session')
async def create_tables(event_loop):
    await init_db()
    await fill_bd_test_data()
    yield
    await drop_db()
