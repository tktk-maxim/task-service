import os
from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from tortoise import Tortoise

from src.main import app
from src.config import settings


@pytest.fixture(scope='session', autouse=True)
def set_test_database_url():
    settings.run_test = True


@pytest.fixture(scope="module")
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c


@pytest.fixture(scope="session", autouse=True)
async def clean_database_after_tests():
    yield
    for model in Tortoise.apps["models"].values():
        await model.all().delete()
