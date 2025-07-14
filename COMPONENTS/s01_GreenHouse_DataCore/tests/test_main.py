import pytest
import os
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app

# Configurar el token para los tests
TEST_TOKEN = os.getenv("SECRET_TOKEN", "test-token-123")

# Test síncrono usando TestClient con autenticación
def test_health_check_sync():
    client = TestClient(app)
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    response = client.get("/health", headers=headers)
    assert response.status_code == 200
    assert response.text == "Hello, its working"
    assert response.headers["content-type"] == "text/plain; charset=utf-8"

# Test asíncrono usando AsyncClient con autenticación
@pytest.mark.asyncio
async def test_health_check_async():
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.get("/health", headers=headers, follow_redirects=True)
        assert response.status_code == 200
        assert response.text == "Hello, its working"
        assert response.headers["content-type"] == "text/plain; charset=utf-8"

# Test con transport personalizado y autenticación
@pytest.mark.asyncio
async def test_health_check_with_transport():
    from httpx import ASGITransport
    
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        response = await ac.get("/health", headers=headers)
        assert response.status_code == 200
        assert response.text == "Hello, its working"
        assert response.headers["content-type"] == "text/plain; charset=utf-8"

# Test para verificar que la autenticación falla sin token
def test_health_check_no_auth():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

# Test para verificar que la autenticación falla con token incorrecto
def test_health_check_wrong_token():
    client = TestClient(app)
    headers = {"Authorization": "Bearer wrong-token"}
    response = client.get("/health", headers=headers)
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

# Fixture para crear un cliente con autenticación automática
@pytest.fixture
def authenticated_client():
    def _client():
        return TestClient(app, headers={"Authorization": f"Bearer {TEST_TOKEN}"})
    return _client

# Ejemplo de uso del fixture
def test_with_fixture(authenticated_client):
    client = authenticated_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "Hello, its working"