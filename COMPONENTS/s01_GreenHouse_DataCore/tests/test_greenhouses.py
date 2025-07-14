import pytest
import os
from fastapi.testclient import TestClient
from httpx import AsyncClient, Response
from app.main import app
import app.controllers.db.db_queries as db_queries

# Configurar el token para los tests
TEST_TOKEN = os.getenv("SECRET_TOKEN", "none")

# Base URL para tests asíncronos
test_base_url = "http://test"

# Fixture para cliente síncrono con cabecera Authorization por defecto
def pytest_configure():
    # Override global auth dependency si existe
    try:
        from app.dependencies import get_current_user
        def fake_get_current_user(token: str = Header(..., alias="Authorization")):
            return {"sub": "test-user"}
        app.dependency_overrides[get_current_user] = fake_get_current_user
    except ImportError:
        pass

@pytest.fixture
def client():
    return TestClient(
        app,
        headers={"Authorization": f"Bearer {TEST_TOKEN}"}
    )

# Fixture para cliente asíncrono con cabecera Authorization por defecto
def _async_client():
    return AsyncClient(
        app=app,
        base_url=test_base_url,
        headers={"Authorization": f"Bearer {TEST_TOKEN}"}
    )

@pytest.fixture
def async_client():
    async def _client():
        async with _async_client() as ac:
            yield ac
    return _client

# 1. Test GET /db/gh/ con headers Authorization y UserAuth
@pytest.mark.asyncio
async def test_get_all_greenhouses_info(async_client, monkeypatch):
    dummy = [{"id": 1, "name": "GH1"}, {"id": 2, "name": "GH2"}]
    monkeypatch.setattr(db_queries, 'get_greenhouses', lambda uid: dummy)
    headers = {"UserAuth": "user123"}
    ac = await async_client()
    response: Response = await ac.get("/db/gh/", headers=headers)
    assert response.status_code == 200
    assert response.json() == dummy

# 2. Test GET /db/gh/ sin UserAuth -> 422
@pytest.mark.asyncio
async def test_get_all_greenhouses_info_missing_header(async_client):
    ac = await async_client()
    response = await ac.get("/db/gh/")
    assert response.status_code == 422

# 3. Test GET /db/gh/{id}
@pytest.mark.asyncio
async def test_get_greenhouse_info_by_id(async_client, monkeypatch):
    dummy = {"id": 5, "name": "TestGH"}
    monkeypatch.setattr(db_queries, 'get_greenhouse', lambda _id: dummy)
    ac = await async_client()
    response = await ac.get("/db/gh/5")
    assert response.status_code == 200
    assert response.json() == dummy

# 4. Test POST /db/gh/ crear greenhouse
@pytest.mark.asyncio
async def test_create_greenhouse(async_client, monkeypatch):
    input_payload = {
        "date": "2025-07-14",
        "name": "NewGH",
        "description": "Test desc",
        "image": None,
        "ip": "127.0.0.1",
        "sync_code": "SC123"
    }
    dummy_response = {"result": "created"}
    monkeypatch.setattr(
        db_queries,
        'create_greenhouse',
        lambda date, name, description, image, ip, sync_code: dummy_response
    )
    ac = await async_client()
    response = await ac.post("/db/gh/", json=input_payload)
    assert response.status_code == 200
    assert response.json() == dummy_response

# 5. Test POST /db/gh/ con campo faltante -> 422
@pytest.mark.asyncio
async def test_create_greenhouse_missing_field(async_client):
    ac = await async_client()
    response = await ac.post("/db/gh/", json={"date": "2025-07-14", "name": "GH"})
    assert response.status_code == 422

# 6. Test POST /db/syncgh/ sincronizar greenhouse
@pytest.mark.asyncio
async def test_sync_greenhouse(async_client, monkeypatch):
    payload = {"name": "SyncGH", "sync_code": "SYNC123"}
    dummy_response = {"result": "synced"}
    monkeypatch.setattr(
        db_queries,
        'sync_greenhouse',
        lambda name, sync_code, owner_id: dummy_response
    )
    headers = {"UserAuth": "owner42"}
    ac = await async_client()
    response = await ac.post("/db/syncgh/", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json() == dummy_response

# 7. Test POST /db/syncgh/ sin UserAuth -> 422
@pytest.mark.asyncio
async def test_sync_greenhouse_missing_header(async_client):
    ac = await async_client()
    response = await ac.post("/db/syncgh/", json={"name": "X", "sync_code": "Y"})
    assert response.status_code == 422

# 8. Test POST /db/syncgh/ sin campo body -> 422
@pytest.mark.asyncio
async def test_sync_greenhouse_missing_body(async_client):
    headers = {"UserAuth": "owner42"}
    ac = await async_client()
    response = await ac.post("/db/syncgh/", headers=headers, json={"name": "X"})
    assert response.status_code == 422
