import pytest
import time
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager
from src.main import app


class TestSyncEndpoints:
    client = TestClient(app)

    def test_sync_route(self):
        response = self.client.post("/Sync")
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    def test_sync_func(self):
        response = self.client.get("/sync/1")
        assert response.status_code == 200

    def test_sync_func_time(self):
        start_time = time.time()
        self.client.get("/sync/1")
        end_time = time.time()
        assert end_time - start_time >= 3  # Проверяем, что функция заняла не менее 3 секунд


class TestAsyncEndpoints:
    @pytest.mark.asyncio
    async def test_async_route(self):
        async with LifespanManager(app):  # Корректный запуск FastAPI
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.post("/Async")
                assert response.status_code == 200
                assert response.json() == {"ok": True}

    @pytest.mark.asyncio
    async def test_async_func(self):
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.get("/async/1")
                assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_async_func_time(self):
        start_time = time.time()
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                await ac.get("/async/1")
        end_time = time.time()
        assert end_time - start_time >= 3  # Проверяем, что функция заняла не менее 3 секунд