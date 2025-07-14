import pytest
import os
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

# Configurar el token para los tests
TEST_TOKEN = os.getenv("SECRET_TOKEN", "none")

# Mock data para los tests
MOCK_GREENHOUSE_DATA = {
    "id": 1,
    "date": "2024-01-01",
    "name": "Test Greenhouse",
    "description": "Test description",
    "image": None,
    "ip": "192.168.1.100",
    "sync_code": "ABC123"
}

MOCK_GREENHOUSES_LIST = [
    MOCK_GREENHOUSE_DATA,
    {
        "id": 2,
        "date": "2024-01-02",
        "name": "Another Greenhouse",
        "description": "Another description",
        "image": None,
        "ip": "192.168.1.101",
        "sync_code": "DEF456"
    }
]

# Fixture para crear un cliente con autenticación automática
@pytest.fixture
def authenticated_client():
    def _client():
        return TestClient(app, headers={"Authorization": f"Bearer {TEST_TOKEN}"})
    return _client

# Tests para GET /db/gh/ - Obtener todos los greenhouses
@patch('app.controllers.db.db_queries.get_greenhouses')
def test_get_all_greenhouses_success(mock_get_greenhouses, authenticated_client):
    mock_get_greenhouses.return_value = MOCK_GREENHOUSES_LIST
    
    client = authenticated_client()
    headers = {"UserAuth": "test_user_id"}
    response = client.get("/db/gh/", headers=headers)
    
    assert response.status_code == 200
    assert response.json() == MOCK_GREENHOUSES_LIST
    mock_get_greenhouses.assert_called_once_with("test_user_id")

@patch('app.controllers.db.db_queries.get_greenhouses')
def test_get_all_greenhouses_empty_list(mock_get_greenhouses, authenticated_client):
    mock_get_greenhouses.return_value = []
    
    client = authenticated_client()
    headers = {"UserAuth": "test_user_id"}
    response = client.get("/db/gh/", headers=headers)
    
    assert response.status_code == 200
    assert response.json() == []
    mock_get_greenhouses.assert_called_once_with("test_user_id")

def test_get_all_greenhouses_missing_user_auth(authenticated_client):
    client = authenticated_client()
    response = client.get("/db/gh/")
    
    assert response.status_code == 422
    assert "field required" in response.json()["detail"][0]["msg"]

def test_get_all_greenhouses_wrong_token():
    client = TestClient(app)
    headers = {"Authorization": "Bearer wrong-token", "UserAuth": "test_user_id"}
    response = client.get("/db/gh/", headers=headers)
    
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

# Tests para GET /db/gh/{id} - Obtener greenhouse por ID
@patch('app.controllers.db.db_queries.get_greenhouse')
def test_get_greenhouse_by_id_success(mock_get_greenhouse, authenticated_client):
    mock_get_greenhouse.return_value = MOCK_GREENHOUSE_DATA
    
    client = authenticated_client()
    response = client.get("/db/gh/1")
    
    assert response.status_code == 200
    assert response.json() == MOCK_GREENHOUSE_DATA
    mock_get_greenhouse.assert_called_once_with(1)

@patch('app.controllers.db.db_queries.get_greenhouse')
def test_get_greenhouse_by_id_not_found(mock_get_greenhouse, authenticated_client):
    mock_get_greenhouse.return_value = None
    
    client = authenticated_client()
    response = client.get("/db/gh/999")
    
    assert response.status_code == 200
    assert response.json() is None
    mock_get_greenhouse.assert_called_once_with(999)

def test_get_greenhouse_by_id_invalid_id(authenticated_client):
    client = authenticated_client()
    response = client.get("/db/gh/invalid")
    
    assert response.status_code == 422
    assert "value is not a valid integer" in str(response.json()["detail"])

def test_get_greenhouse_by_id_wrong_token():
    client = TestClient(app)
    headers = {"Authorization": "Bearer wrong-token"}
    response = client.get("/db/gh/1", headers=headers)
    
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

# Tests para POST /db/gh/ - Crear greenhouse
@patch('app.controllers.db.db_queries.create_greenhouse')
def test_create_greenhouse_success(mock_create_greenhouse, authenticated_client):
    mock_create_greenhouse.return_value = {"id": 1, "status": "created"}
    
    client = authenticated_client()
    greenhouse_data = {
        "date": "2024-01-01",
        "name": "New Greenhouse",
        "description": "New description",
        "ip": "192.168.1.200",
        "sync_code": "XYZ789"
    }
    
    response = client.post("/db/gh/", json=greenhouse_data)
    
    assert response.status_code == 200
    assert response.json() == {"id": 1, "status": "created"}
    mock_create_greenhouse.assert_called_once_with(
        date="2024-01-01",
        name="New Greenhouse",
        description="New description",
        image=None,
        ip="192.168.1.200",
        sync_code="XYZ789"
    )

@patch('app.controllers.db.db_queries.create_greenhouse')
def test_create_greenhouse_minimal_data(mock_create_greenhouse, authenticated_client):
    mock_create_greenhouse.return_value = {"id": 2, "status": "created"}
    
    client = authenticated_client()
    greenhouse_data = {
        "date": "2024-01-01",
        "name": "Minimal Greenhouse",
        "sync_code": "MIN123"
    }
    
    response = client.post("/db/gh/", json=greenhouse_data)
    
    assert response.status_code == 200
    assert response.json() == {"id": 2, "status": "created"}
    mock_create_greenhouse.assert_called_once_with(
        date="2024-01-01",
        name="Minimal Greenhouse",
        description=None,
        image=None,
        ip=None,
        sync_code="MIN123"
    )

def test_create_greenhouse_missing_required_fields(authenticated_client):
    client = authenticated_client()
    greenhouse_data = {
        "name": "Incomplete Greenhouse"
        # Faltan date y sync_code
    }
    
    response = client.post("/db/gh/", json=greenhouse_data)
    
    assert response.status_code == 422
    assert "field required" in str(response.json()["detail"])

def test_create_greenhouse_empty_name(authenticated_client):
    client = authenticated_client()
    greenhouse_data = {
        "date": "2024-01-01",
        "name": "",
        "sync_code": "ABC123"
    }
    
    response = client.post("/db/gh/", json=greenhouse_data)
    
    assert response.status_code == 422

def test_create_greenhouse_wrong_token():
    client = TestClient(app)
    headers = {"Authorization": "Bearer wrong-token"}
    greenhouse_data = {
        "date": "2024-01-01",
        "name": "Test Greenhouse",
        "sync_code": "ABC123"
    }
    
    response = client.post("/db/gh/", json=greenhouse_data, headers=headers)
    
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

# Tests para POST /db/syncgh/ - Sincronizar greenhouse
@patch('app.controllers.db.db_queries.sync_greenhouse')
def test_sync_greenhouse_success(mock_sync_greenhouse, authenticated_client):
    mock_sync_greenhouse.return_value = {"status": "synced", "greenhouse_id": 1}
    
    client = authenticated_client()
    sync_data = {
        "name": "Sync Greenhouse",
        "sync_code": "SYNC123"
    }
    headers = {"UserAuth": "test_user_id"}
    
    response = client.post("/db/syncgh/", json=sync_data, headers=headers)
    
    assert response.status_code == 200
    assert response.json() == {"status": "synced", "greenhouse_id": 1}
    mock_sync_greenhouse.assert_called_once_with(
        name="Sync Greenhouse",
        sync_code="SYNC123",
        owner_id="test_user_id"
    )

@patch('app.controllers.db.db_queries.sync_greenhouse')
def test_sync_greenhouse_not_found(mock_sync_greenhouse, authenticated_client):
    mock_sync_greenhouse.return_value = {"status": "not_found", "error": "Greenhouse not found"}
    
    client = authenticated_client()
    sync_data = {
        "name": "Nonexistent Greenhouse",
        "sync_code": "NOTFOUND123"
    }
    headers = {"UserAuth": "test_user_id"}
    
    response = client.post("/db/syncgh/", json=sync_data, headers=headers)
    
    assert response.status_code == 200
    assert response.json() == {"status": "not_found", "error": "Greenhouse not found"}
    mock_sync_greenhouse.assert_called_once_with(
        name="Nonexistent Greenhouse",
        sync_code="NOTFOUND123",
        owner_id="test_user_id"
    )

def test_sync_greenhouse_missing_required_fields(authenticated_client):
    client = authenticated_client()
    sync_data = {
        "name": "Incomplete Sync"
        # Falta sync_code
    }
    headers = {"UserAuth": "test_user_id"}
    
    response = client.post("/db/syncgh/", json=sync_data, headers=headers)
    
    assert response.status_code == 422
    assert "field required" in str(response.json()["detail"])

def test_sync_greenhouse_missing_user_auth(authenticated_client):
    client = authenticated_client()
    sync_data = {
        "name": "Sync Greenhouse",
        "sync_code": "SYNC123"
    }
    
    response = client.post("/db/syncgh/", json=sync_data)
    
    assert response.status_code == 422
    assert "field required" in response.json()["detail"][0]["msg"]

def test_sync_greenhouse_wrong_token():
    client = TestClient(app)
    headers = {"Authorization": "Bearer wrong-token", "UserAuth": "test_user_id"}
    sync_data = {
        "name": "Sync Greenhouse",
        "sync_code": "SYNC123"
    }
    
    response = client.post("/db/syncgh/", json=sync_data, headers=headers)
    
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

# Tests asíncronos con AsyncClient
@pytest.mark.asyncio
@patch('app.controllers.db.db_queries.get_greenhouses')
async def test_get_all_greenhouses_async(mock_get_greenhouses):
    from httpx import ASGITransport
    
    mock_get_greenhouses.return_value = MOCK_GREENHOUSES_LIST
    
    headers = {
        "Authorization": f"Bearer {TEST_TOKEN}",
        "UserAuth": "async_user_id"
    }
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        response = await ac.get("/db/gh/", headers=headers)
        assert response.status_code == 200
        assert response.json() == MOCK_GREENHOUSES_LIST
        mock_get_greenhouses.assert_called_once_with("async_user_id")

@pytest.mark.asyncio
@patch('app.controllers.db.db_queries.create_greenhouse')
async def test_create_greenhouse_async(mock_create_greenhouse):
    from httpx import ASGITransport
    
    mock_create_greenhouse.return_value = {"id": 1, "status": "created"}
    
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    greenhouse_data = {
        "date": "2024-01-01",
        "name": "Async Greenhouse",
        "sync_code": "ASYNC123"
    }
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        response = await ac.post("/db/gh/", json=greenhouse_data, headers=headers)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "status": "created"}
        mock_create_greenhouse.assert_called_once_with(
            date="2024-01-01",
            name="Async Greenhouse",
            description=None,
            image=None,
            ip=None,
            sync_code="ASYNC123"
        )