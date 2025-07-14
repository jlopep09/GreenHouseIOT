import pytest
import os
from unittest.mock import patch, MagicMock
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
import mariadb

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

# Mock data para los tests
@pytest.fixture
def mock_actuator_data():
    return {
        "name": "pump",
        "gh_id": 1,
        "auto": True,
        "timer_on": "09:00:00",
        "timer_off": "14:00:00",
        "manual_status": False
    }

@pytest.fixture
def mock_db_configs():
    return {
        "configs": [
            {
                "id": 1,
                "name": "pump",
                "auto": 1,
                "timer_on": "09:00:00",
                "timer_off": "14:00:00",
                "manual_status": 0,
                "gh_id": 1
            },
            {
                "id": 2,
                "name": "fan",
                "auto": 0,
                "timer_on": "10:00:00",
                "timer_off": "16:00:00",
                "manual_status": 1,
                "gh_id": 1
            }
        ]
    }

@pytest.fixture
def mock_db_reads():
    return [
        {
            "id": 1,
            "temperature": 25.5,
            "humidity": 65.0,
            "ph": 7.2,
            "timestamp": "2024-01-15T10:30:00",
            "gh_id": 1
        },
        {
            "id": 2,
            "temperature": 26.0,
            "humidity": 60.0,
            "ph": 7.0,
            "timestamp": "2024-01-15T11:30:00",
            "gh_id": 1
        }
    ]

# ==========================================
# Tests para GET /db/reads/
# ==========================================

@patch('app.controllers.db.db_queries.get_reads')
def test_get_all_reads_success(mock_get_reads, authenticated_client, mock_db_reads):
    """Test exitoso para obtener todas las lecturas"""
    mock_get_reads.return_value = mock_db_reads
    client = authenticated_client()
    
    response = client.get("/db/reads/", headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 200
    assert response.json() == mock_db_reads
    mock_get_reads.assert_called_once_with("test_user_123")

@patch('app.controllers.db.db_queries.get_reads')
def test_get_all_reads_empty(mock_get_reads, authenticated_client):
    """Test cuando no hay lecturas"""
    mock_get_reads.return_value = []
    client = authenticated_client()
    
    response = client.get("/db/reads/", headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 200
    assert response.json() == []

def test_get_all_reads_missing_auth_header(authenticated_client):
    """Test cuando falta el header de autenticación UserAuth"""
    client = authenticated_client()
    
    response = client.get("/db/reads/")
    
    assert response.status_code == 422  # Unprocessable Entity por header requerido

def test_get_all_reads_wrong_token():
    """Test con token de autorización incorrecto"""
    client = TestClient(app, headers={"Authorization": "Bearer wrong-token"})
    
    response = client.get("/db/reads/", headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 403

# ==========================================
# Tests para GET /db/ghconfig/
# ==========================================

@patch('app.controllers.db.connector.get_con')
def test_get_ghconfigs_success(mock_get_con, authenticated_client):
    """Test exitoso para obtener configuraciones de invernaderos"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock para obtener IDs de invernaderos
    mock_cursor.fetchall.side_effect = [
        [(1,), (2,)],  # IDs de invernaderos
        [  # Datos de actuadores
            (1, "pump", b'\x01', "09:00:00", "14:00:00", b'\x00', 1),
            (2, "fan", b'\x00', "10:00:00", "16:00:00", b'\x01', 1)
        ]
    ]
    
    mock_cursor.description = [
        ("id",), ("name",), ("auto",), ("timer_on",), ("timer_off",), ("manual_status",), ("gh_id",)
    ]
    
    client = authenticated_client()
    response = client.get("/db/ghconfig/", headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 200
    data = response.json()
    assert "configs" in data
    assert len(data["configs"]) == 2
    assert data["configs"][0]["auto"] == 1
    assert data["configs"][0]["manual_status"] == 0
    assert data["configs"][1]["auto"] == 0
    assert data["configs"][1]["manual_status"] == 1

@patch('app.controllers.db.connector.get_con')
def test_get_ghconfigs_no_greenhouses(mock_get_con, authenticated_client):
    """Test cuando el usuario no tiene invernaderos"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = []  # Sin invernaderos
    
    client = authenticated_client()
    response = client.get("/db/ghconfig/", headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 200
    data = response.json()
    assert data == {"configs": []}

@patch('app.controllers.db.connector.get_con')
def test_get_ghconfigs_database_error(mock_get_con, authenticated_client):
    """Test manejo de errores de base de datos"""
    mock_get_con.side_effect = mariadb.Error("Database connection failed")
    
    client = authenticated_client()
    response = client.get("/db/ghconfig/", headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 500
    assert "Failed to retrieve configs" in response.json()["detail"]

@patch('app.controllers.db.connector.get_con')
def test_get_ghconfigs_string_bit_fields(mock_get_con, authenticated_client):
    """Test normalización de campos BIT que vienen como string"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.side_effect = [
        [(1,)],  # IDs de invernaderos
        [(1, "pump", "\x01", "09:00:00", "14:00:00", "\x00", 1)]  # String bit fields
    ]
    
    mock_cursor.description = [
        ("id",), ("name",), ("auto",), ("timer_on",), ("timer_off",), ("manual_status",), ("gh_id",)
    ]
    
    client = authenticated_client()
    response = client.get("/db/ghconfig/", headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["configs"][0]["auto"] == 1
    assert data["configs"][0]["manual_status"] == 0

# ==========================================
# Tests para GET /db/reads/{id}
# ==========================================

@patch('app.controllers.db.db_queries.get_reads_byid')
def test_get_reads_from_greenhouse_id_success(mock_get_reads_byid, authenticated_client):
    """Test exitoso para obtener lecturas por ID de invernadero"""
    mock_reads = [
        {"id": 1, "temperature": 25.5, "humidity": 65.0, "gh_id": 1},
        {"id": 2, "temperature": 26.0, "humidity": 60.0, "gh_id": 1}
    ]
    mock_get_reads_byid.return_value = mock_reads
    
    client = authenticated_client()
    response = client.get("/db/reads/1")
    
    assert response.status_code == 200
    assert response.json() == mock_reads
    mock_get_reads_byid.assert_called_once_with(1)

@patch('app.controllers.db.db_queries.get_reads_byid')
def test_get_reads_from_greenhouse_id_empty(mock_get_reads_byid, authenticated_client):
    """Test cuando no hay lecturas para el ID especificado"""
    mock_get_reads_byid.return_value = []
    
    client = authenticated_client()
    response = client.get("/db/reads/999")
    
    assert response.status_code == 200
    assert response.json() == []
    mock_get_reads_byid.assert_called_once_with(999)

def test_get_reads_from_greenhouse_id_invalid_id(authenticated_client):
    """Test con ID inválido"""
    client = authenticated_client()
    response = client.get("/db/reads/invalid")
    
    assert response.status_code == 422  # Validation error

# ==========================================
# Tests para POST /db/ghconfig/
# ==========================================

@patch('app.controllers.db.connector.get_con')
def test_create_actuator_config_success(mock_get_con, authenticated_client):
    """Test exitoso para crear configuración de actuador"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock para verificar que el invernadero pertenece al usuario
    mock_cursor.fetchone.return_value = (1,)
    mock_cursor.lastrowid = 5
    
    client = authenticated_client()
    actuator_data = {
        "name": "pump",
        "gh_id": 1,
        "auto": True,
        "timer_on": "09:00:00",
        "timer_off": "14:00:00",
        "manual_status": False
    }
    
    response = client.post("/db/ghconfig/", json=actuator_data, headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 5
    assert data["message"] == "Actuador creado exitosamente"
    assert data["actuator"]["name"] == "pump"
    assert data["actuator"]["auto"] == True
    assert data["actuator"]["manual_status"] == False

@patch('app.controllers.db.connector.get_con')
def test_create_actuator_config_minimal_data(mock_get_con, authenticated_client):
    """Test crear actuador con datos mínimos (valores por defecto)"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = (1,)
    mock_cursor.lastrowid = 6
    
    client = authenticated_client()
    actuator_data = {
        "name": "fan",
        "gh_id": 1
    }
    
    response = client.post("/db/ghconfig/", json=actuator_data, headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["actuator"]["auto"] == False  # Valor por defecto
    assert data["actuator"]["timer_on"] == "09:00:00"  # Valor por defecto
    assert data["actuator"]["timer_off"] == "14:00:00"  # Valor por defecto
    assert data["actuator"]["manual_status"] == False  # Valor por defecto

def test_create_actuator_config_missing_required_fields(authenticated_client):
    """Test cuando faltan campos requeridos"""
    client = authenticated_client()
    
    # Falta 'name'
    actuator_data = {"gh_id": 1}
    response = client.post("/db/ghconfig/", json=actuator_data, headers={"UserAuth": "test_user_123"})
    assert response.status_code == 400
    assert "Campo requerido faltante: name" in response.json()["detail"]
    
    # Falta 'gh_id'
    actuator_data = {"name": "pump"}
    response = client.post("/db/ghconfig/", json=actuator_data, headers={"UserAuth": "test_user_123"})
    assert response.status_code == 400
    assert "Campo requerido faltante: gh_id" in response.json()["detail"]

def test_create_actuator_config_invalid_name(authenticated_client):
    """Test con nombre de actuador inválido"""
    client = authenticated_client()
    actuator_data = {
        "name": "invalid_actuator",
        "gh_id": 1
    }
    
    response = client.post("/db/ghconfig/", json=actuator_data, headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 400
    assert "Nombre de actuador inválido" in response.json()["detail"]
    assert "pump, fan, light, oxigen" in response.json()["detail"]

@patch('app.controllers.db.connector.get_con')
def test_create_actuator_config_unauthorized_greenhouse(mock_get_con, authenticated_client):
    """Test cuando el invernadero no pertenece al usuario"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = None  # Invernadero no encontrado
    
    client = authenticated_client()
    actuator_data = {
        "name": "pump",
        "gh_id": 999
    }
    
    response = client.post("/db/ghconfig/", json=actuator_data, headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 403
    assert "No tienes permiso para modificar este invernadero" in response.json()["detail"]

@patch('app.controllers.db.connector.get_con')
def test_create_actuator_config_database_error(mock_get_con, authenticated_client):
    """Test manejo de errores de base de datos en creación"""
    mock_get_con.side_effect = mariadb.Error("Database error")
    
    client = authenticated_client()
    actuator_data = {
        "name": "pump",
        "gh_id": 1
    }
    
    response = client.post("/db/ghconfig/", json=actuator_data, headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 500
    assert "Error al crear configuración" in response.json()["detail"]

# ==========================================
# Tests para PUT /db/ghconfig/{actuator_id}
# ==========================================

@patch('app.controllers.db.connector.get_con')
def test_update_actuator_config_success(mock_get_con, authenticated_client):
    """Test exitoso para actualizar configuración de actuador"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock para verificar que el actuador pertenece al usuario
    mock_cursor.fetchone.return_value = (1,)
    mock_cursor.rowcount = 1  # Indica que se modificó una fila
    
    client = authenticated_client()
    actuator_data = {
        "name": "pump",
        "gh_id": 1,
        "auto": True,
        "timer_on": "08:00:00",
        "timer_off": "18:00:00",
        "manual_status": True
    }
    
    response = client.put("/db/ghconfig/1", json=actuator_data, headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["message"] == "Actuador actualizado exitosamente"
    assert data["actuator"]["timer_on"] == "08:00:00"
    assert data["actuator"]["timer_off"] == "18:00:00"
    assert data["actuator"]["manual_status"] == True

def test_update_actuator_config_missing_required_fields(authenticated_client):
    """Test cuando faltan campos requeridos en actualización"""
    client = authenticated_client()
    
    # Falta varios campos requeridos
    actuator_data = {"name": "pump"}
    response = client.put("/db/ghconfig/1", json=actuator_data, headers={"UserAuth": "test_user_123"})
    assert response.status_code == 400
    assert "Campo requerido faltante" in response.json()["detail"]

def test_update_actuator_config_invalid_name(authenticated_client):
    """Test actualización con nombre inválido"""
    client = authenticated_client()
    actuator_data = {
        "name": "invalid_name",
        "gh_id": 1,
        "auto": True,
        "timer_on": "08:00:00",
        "timer_off": "18:00:00",
        "manual_status": True
    }
    
    response = client.put("/db/ghconfig/1", json=actuator_data, headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 400
    assert "Nombre de actuador inválido" in response.json()["detail"]

@patch('app.controllers.db.connector.get_con')
def test_update_actuator_config_unauthorized(mock_get_con, authenticated_client):
    """Test cuando el actuador no pertenece al usuario"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_con.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = None  # Actuador no encontrado
    
    client = authenticated_client()
    actuator_data = {
        "name": "pump",
        "gh_id": 1,
        "auto": True,
        "timer_on": "08:00:00",
        "timer_off": "18:00:00",
        "manual_status": True
    }
    
    response = client.put("/db/ghconfig/999", json=actuator_data, headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 403
    assert "No tienes permiso para modificar este actuador" in response.json()["detail"]


@patch('app.controllers.db.connector.get_con')
def test_update_actuator_config_database_error(mock_get_con, authenticated_client):
    """Test manejo de errores de base de datos en actualización"""
    mock_get_con.side_effect = mariadb.Error("Database error")
    
    client = authenticated_client()
    actuator_data = {
        "name": "pump",
        "gh_id": 1,
        "auto": True,
        "timer_on": "08:00:00",
        "timer_off": "18:00:00",
        "manual_status": True
    }
    
    response = client.put("/db/ghconfig/1", json=actuator_data, headers={"UserAuth": "test_user_123"})
    
    assert response.status_code == 500
    assert "Error al actualizar configuración" in response.json()["detail"]


# ==========================================
# Tests de casos edge y robustez
# ==========================================

def test_all_valid_actuator_names(authenticated_client):
    """Test que todos los nombres de actuadores válidos sean aceptados"""
    valid_names = ['pump', 'fan', 'light', 'oxigen']
    
    for name in valid_names:
        actuator_data = {
            "name": name,
            "gh_id": 1,
            "auto": True,
            "timer_on": "08:00:00",
            "timer_off": "18:00:00",
            "manual_status": True
        }
        
        # Solo verificamos que la validación pase, no ejecutamos la lógica completa
        client = authenticated_client()
        with patch('app.controllers.db.connector.get_con') as mock_get_con:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_get_con.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = (1,)
            mock_cursor.rowcount = 1
            
            response = client.put("/db/ghconfig/1", json=actuator_data, headers={"UserAuth": "test_user_123"})
            assert response.status_code == 200