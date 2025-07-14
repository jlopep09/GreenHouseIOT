import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.text == "Hello, its working"
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
