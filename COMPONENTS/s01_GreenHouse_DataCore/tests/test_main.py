import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app

# Test síncrono usando TestClient (más simple)
def test_health_check_sync():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "Hello, its working"
    assert response.headers["content-type"] == "text/plain; charset=utf-8"

# Test asíncrono usando AsyncClient
@pytest.mark.asyncio
async def test_health_check_async():
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.get("/health", follow_redirects=True)
        assert response.status_code == 200
        assert response.text == "Hello, its working"
        assert response.headers["content-type"] == "text/plain; charset=utf-8"

# Alternativa usando transport personalizado
@pytest.mark.asyncio
async def test_health_check_with_transport():
    from httpx import ASGITransport
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.text == "Hello, its working"
        assert response.headers["content-type"] == "text/plain; charset=utf-8"