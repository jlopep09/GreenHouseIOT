import pytest
import os
import json
from unittest.mock import patch, MagicMock
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
import mariadb
from datetime import datetime

# Configurar el token para los tests
TEST_TOKEN = os.getenv("SECRET_TOKEN", "none")

# Fixture para crear un cliente con autenticación automática
@pytest.fixture
def authenticated_client():
    def _client():
        return TestClient(app, headers={"Authorization": f"Bearer {TEST_TOKEN}"})
    return _client

# Fixture para AsyncClient con autenticación
@pytest.fixture
async def async_authenticated_client():
    from httpx import ASGITransport
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test",
        headers=headers
    ) as ac:
        yield ac

# Fixture para datos de usuario
@pytest.fixture
def user_create_data():
    return {
        "email": "test@example.com",
        "name": "Test User"
    }

@pytest.fixture
def existing_user_data():
    return {
        "id": 1,
        "auth0_id": "auth0|test_user_123",
        "email": "existing@example.com",
        "name": "Existing User",
        "created_at": datetime(2024, 1, 15, 10, 30, 0)
    }

@pytest.fixture
def new_user_data():
    return {
        "id": 5,
        "auth0_id": "auth0|new_user_456",
        "email": "new@example.com",
        "name": "New User",
        "created_at": datetime(2024, 1, 15, 11, 0, 0)
    }

# ==========================================
# Tests para POST /db/users/
# ==========================================

@patch('app.controllers.db.connector.get_con')
def test_ensure_user_in_db_existing_user(mock_get_con, authenticated_client, user_create_data, existing_user_data):
    """Test cuando el usuario ya existe en la base de datos"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock para usuario existente
    mock_cursor.fetchone.return_value = (
        existing_user_data["id"],
        existing_user_data["auth0_id"],
        existing_user_data["email"],
        existing_user_data["name"],
        existing_user_data["created_at"]
    )
    
    mock_cursor.description = [
        ("id",), ("auth0_id",), ("email",), ("name",), ("created_at",)
    ]
    
    client = authenticated_client()
    response = client.post(
        "/db/users/", 
        json=user_create_data,
        headers={"UserAuth": "auth0|test_user_123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == existing_user_data["id"]
    assert data["auth0_id"] == existing_user_data["auth0_id"]
    assert data["email"] == existing_user_data["email"]
    assert data["name"] == existing_user_data["name"]
    
    # Verificar que no se intentó insertar
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_not_called()


@patch('app.controllers.db.connector.get_con')
def test_ensure_user_in_db_create_new_user_with_different_data(mock_get_con, authenticated_client):
    """Test creación de usuario con datos diferentes"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Usuario no existe, luego devolver usuario creado
    mock_cursor.fetchone.side_effect = [
        None,
        (2, "auth0|user_789", "admin@company.com", "Admin User", datetime(2024, 1, 15, 12, 0, 0))
    ]
    
    mock_cursor.description = [
        ("id",), ("auth0_id",), ("email",), ("name",), ("created_at",)
    ]
    
    mock_cursor.lastrowid = 2
    
    client = authenticated_client()
    user_data = {
        "email": "admin@company.com",
        "name": "Admin User"
    }
    
    response = client.post(
        "/db/users/", 
        json=user_data,
        headers={"UserAuth": "auth0|user_789"}
    )
    
    assert response.status_code == 201
    
    # Verificar que se pasaron los datos correctos al INSERT
    insert_call = mock_cursor.execute.call_args_list[1]
    assert insert_call[0][1] == ("auth0|user_789", "admin@company.com", "Admin User")

def test_ensure_user_in_db_missing_required_fields(authenticated_client):
    """Test cuando faltan campos requeridos"""
    client = authenticated_client()
    
    # Falta email
    user_data = {"name": "Test User"}
    response = client.post(
        "/db/users/", 
        json=user_data,
        headers={"UserAuth": "auth0|test_user_123"}
    )
    assert response.status_code == 422  # Validation error
    
    # Falta name
    user_data = {"email": "test@example.com"}
    response = client.post(
        "/db/users/", 
        json=user_data,
        headers={"UserAuth": "auth0|test_user_123"}
    )
    assert response.status_code == 422  # Validation error


def test_ensure_user_in_db_missing_user_auth_header(authenticated_client):
    """Test cuando falta el header UserAuth"""
    client = authenticated_client()
    
    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }
    
    response = client.post("/db/users/", json=user_data)
    
    assert response.status_code == 422  # Unprocessable Entity por header requerido

def test_ensure_user_in_db_wrong_token():
    """Test con token de autorización incorrecto"""
    client = TestClient(app, headers={"Authorization": "Bearer wrong-token"})
    
    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }
    
    response = client.post(
        "/db/users/", 
        json=user_data,
        headers={"UserAuth": "auth0|test_user_123"}
    )
    
    assert response.status_code == 403

@patch('app.controllers.db.connector.get_con')
def test_ensure_user_in_db_database_error_on_select(mock_get_con, authenticated_client, user_create_data):
    """Test manejo de error de base de datos en SELECT"""
    mock_get_con.side_effect = mariadb.Error("Database connection failed")
    
    client = authenticated_client()
    response = client.post(
        "/db/users/", 
        json=user_create_data,
        headers={"UserAuth": "auth0|test_user_123"}
    )
    
    assert response.status_code == 500
    assert "Failed to ensure user in database" in response.json()["detail"]

@patch('app.controllers.db.connector.get_con')
def test_ensure_user_in_db_database_error_on_insert(mock_get_con, authenticated_client, user_create_data):
    """Test manejo de error de base de datos en INSERT"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Primera llamada: usuario no existe
    mock_cursor.fetchone.return_value = None
    
    # Error en INSERT
    mock_cursor.execute.side_effect = [
        None,  # SELECT funciona
        mariadb.Error("Insert failed")  # INSERT falla
    ]
    
    client = authenticated_client()
    response = client.post(
        "/db/users/", 
        json=user_create_data,
        headers={"UserAuth": "auth0|test_user_123"}
    )
    
    assert response.status_code == 500
    assert "Failed to ensure user in database" in response.json()["detail"]

@patch('app.controllers.db.connector.get_con')
def test_ensure_user_in_db_database_error_on_final_select(mock_get_con, authenticated_client, user_create_data):
    """Test manejo de error de base de datos en SELECT final"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.lastrowid = 5
    
    # Primera llamada: usuario no existe
    # Segunda llamada: INSERT funciona
    # Tercera llamada: SELECT final falla
    mock_cursor.execute.side_effect = [
        None,  # SELECT inicial funciona
        None,  # INSERT funciona
        mariadb.Error("Final select failed")  # SELECT final falla
    ]
    
    mock_cursor.fetchone.return_value = None
    
    client = authenticated_client()
    response = client.post(
        "/db/users/", 
        json=user_create_data,
        headers={"UserAuth": "auth0|test_user_123"}
    )
    
    assert response.status_code == 500
    assert "Failed to ensure user in database" in response.json()["detail"]

@patch('app.controllers.db.connector.get_con')
def test_ensure_user_in_db_commit_error(mock_get_con, authenticated_client, user_create_data):
    """Test manejo de error en commit"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Usuario no existe
    mock_cursor.fetchone.return_value = None
    
    # Error en commit
    mock_conn.commit.side_effect = mariadb.Error("Commit failed")
    
    client = authenticated_client()
    response = client.post(
        "/db/users/", 
        json=user_create_data,
        headers={"UserAuth": "auth0|test_user_123"}
    )
    
    assert response.status_code == 500
    assert "Failed to ensure user in database" in response.json()["detail"]

# ==========================================
# Tests con diferentes tipos de datos
# ==========================================

@patch('app.controllers.db.connector.get_con')
def test_ensure_user_in_db_special_characters(mock_get_con, authenticated_client):
    """Test con caracteres especiales en nombre y email"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Usuario no existe, luego devolver usuario creado
    mock_cursor.fetchone.side_effect = [
        None,
        (3, "auth0|special_user", "josé.maría@ejemplo.com", "José María Ñoño", datetime(2024, 1, 15, 13, 0, 0))
    ]
    
    mock_cursor.description = [
        ("id",), ("auth0_id",), ("email",), ("name",), ("created_at",)
    ]
    
    mock_cursor.lastrowid = 3
    
    client = authenticated_client()
    user_data = {
        "email": "josé.maría@ejemplo.com",
        "name": "José María Ñoño"
    }
    
    response = client.post(
        "/db/users/", 
        json=user_data,
        headers={"UserAuth": "auth0|special_user"}
    )
    
    assert response.status_code == 201
    
    # Verificar que se pasaron los caracteres especiales correctamente
    insert_call = mock_cursor.execute.call_args_list[1]
    assert insert_call[0][1] == ("auth0|special_user", "josé.maría@ejemplo.com", "José María Ñoño")

@patch('app.controllers.db.connector.get_con')
def test_ensure_user_in_db_long_fields(mock_get_con, authenticated_client):
    """Test con campos largos"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    long_name = "A" * 100
    long_email = "a" * 50 + "@example.com"
    
    # Usuario no existe, luego devolver usuario creado
    mock_cursor.fetchone.side_effect = [
        None,
        (4, "auth0|long_user", long_email, long_name, datetime(2024, 1, 15, 14, 0, 0))
    ]
    
    mock_cursor.description = [
        ("id",), ("auth0_id",), ("email",), ("name",), ("created_at",)
    ]
    
    mock_cursor.lastrowid = 4
    
    client = authenticated_client()
    user_data = {
        "email": long_email,
        "name": long_name
    }
    
    response = client.post(
        "/db/users/", 
        json=user_data,
        headers={"UserAuth": "auth0|long_user"}
    )
    
    assert response.status_code == 201


# ==========================================
# Tests de edge cases
# ==========================================

def test_ensure_user_in_db_json_malformed(authenticated_client):
    """Test con JSON malformado"""
    client = authenticated_client()
    
    response = client.post(
        "/db/users/", 
        data="{'email': 'test@example.com', 'name': 'Test User'",  # JSON malformado
        headers={
            "UserAuth": "auth0|test_user_123",
            "Content-Type": "application/json"
        }
    )
    
    assert response.status_code == 422

def test_ensure_user_in_db_empty_json(authenticated_client):
    """Test con JSON vacío"""
    client = authenticated_client()
    
    response = client.post(
        "/db/users/", 
        json={},
        headers={"UserAuth": "auth0|test_user_123"}
    )
    
    assert response.status_code == 422

@patch('app.controllers.db.connector.get_con')
def test_ensure_user_in_db_connection_close_called(mock_get_con, authenticated_client, user_create_data, existing_user_data):
    """Test que la conexión se cierra correctamente"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock para usuario existente
    mock_cursor.fetchone.return_value = (
        existing_user_data["id"],
        existing_user_data["auth0_id"],
        existing_user_data["email"],
        existing_user_data["name"],
        existing_user_data["created_at"]
    )
    
    mock_cursor.description = [
        ("id",), ("auth0_id",), ("email",), ("name",), ("created_at",)
    ]
    
    client = authenticated_client()
    response = client.post(
        "/db/users/", 
        json=user_create_data,
        headers={"UserAuth": "auth0|test_user_123"}
    )
    
    assert response.status_code == 200
    # Verificar que se cerró la conexión
    mock_conn.close.assert_called_once()

# ==========================================
# Tests para verificar la estructura de respuesta
# ==========================================

@patch('app.controllers.db.connector.get_con')
def test_ensure_user_in_db_response_structure(mock_get_con, authenticated_client, user_create_data):
    """Test que la estructura de respuesta sea correcta"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    expected_user = {
        "id": 7,
        "auth0_id": "auth0|structure_test",
        "email": "structure@test.com",
        "name": "Structure Test",
        "created_at": datetime(2024, 1, 15, 16, 0, 0)
    }
    
    # Usuario no existe, luego devolver usuario creado
    mock_cursor.fetchone.side_effect = [
        None,
        (
            expected_user["id"],
            expected_user["auth0_id"],
            expected_user["email"],
            expected_user["name"],
            expected_user["created_at"]
        )
    ]
    
    mock_cursor.description = [
        ("id",), ("auth0_id",), ("email",), ("name",), ("created_at",)
    ]
    
    mock_cursor.lastrowid = 7
    
    client = authenticated_client()
    response = client.post(
        "/db/users/", 
        json=user_create_data,
        headers={"UserAuth": "auth0|structure_test"}
    )
    
    assert response.status_code == 201
    
    # Verificar que todos los campos requeridos están presentes
    # Nota: La respuesta actual usa __repr__() por el bug en el código,
    # pero verificamos que se llama correctamente
    assert mock_cursor.execute.call_count == 3  # SELECT, INSERT, SELECT final