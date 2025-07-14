import pytest
import os
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock, mock_open
import mariadb
import requests
import base64
import io

# Configurar el token para los tests
TEST_TOKEN = os.getenv("SECRET_TOKEN", "none")

# Mock data para los tests
MOCK_IMAGE_BYTES = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
MOCK_IMAGE_BASE64 = base64.b64encode(MOCK_IMAGE_BYTES).decode("utf-8")

# Fixture para crear un cliente con autenticación automática
@pytest.fixture
def authenticated_client():
    def _client():
        return TestClient(app, headers={"Authorization": f"Bearer {TEST_TOKEN}"})
    return _client

# Tests para GET /db/initkafka
@patch('app.kafka_module.consumer.consume_messages')
def test_init_kafka_success(mock_consume_messages, authenticated_client):
    """Test inicialización exitosa de Kafka"""
    mock_consume_messages.return_value = None
    
    client = authenticated_client()
    response = client.get("/db/initkafka")
    
    assert response.status_code == 200
    assert response.text == "Kafka consumiendo mensajes del topic"
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    mock_consume_messages.assert_called_once()


def test_init_kafka_wrong_token():
    """Test con token de autenticación incorrecto"""
    client = TestClient(app)
    headers = {"Authorization": "Bearer wrong-token"}
    response = client.get("/db/initkafka", headers=headers)
    
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

# Tests para POST /db/img/forward-last
@patch('app.controllers.db.connector.get_con')
@patch('requests.post')
def test_forward_last_img_success(mock_requests_post, mock_get_con, authenticated_client):
    """Test exitoso de reenvío de última imagen"""
    # Mock database
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (1, MOCK_IMAGE_BYTES)
    mock_conn.cursor.return_value = mock_cur
    mock_get_con.return_value = mock_conn
    
    # Mock requests response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"analysis": "Healthy crop detected"}
    mock_response.headers = {"Content-Type": "application/json"}
    mock_requests_post.return_value = mock_response
    
    client = authenticated_client()
    response = client.post(
        "/db/img/forward-last",
        data={
            "prompt": "Analyze this crop",
            "temperature": "0.5",
            "max_tokens": "1500"
        }
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["analysis"] == "Healthy crop detected"
    assert result["image_id"] == 1
    
    # Verificar llamadas a DB
    mock_cur.execute.assert_called_once_with("SELECT id, image FROM images ORDER BY id DESC LIMIT 1")
    mock_cur.fetchone.assert_called_once()
    mock_cur.close.assert_called_once()
    mock_conn.close.assert_called_once()
    
    # Verificar llamada a requests
    mock_requests_post.assert_called_once()

@patch('app.controllers.db.connector.get_con')
@patch('requests.post')
def test_forward_last_img_default_values(mock_requests_post, mock_get_con, authenticated_client):
    """Test con valores por defecto de temperature y max_tokens"""
    # Mock database
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (1, MOCK_IMAGE_BYTES)
    mock_conn.cursor.return_value = mock_cur
    mock_get_con.return_value = mock_conn
    
    # Mock requests response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"analysis": "Default analysis"}
    mock_response.headers = {"Content-Type": "application/json"}
    mock_requests_post.return_value = mock_response
    
    client = authenticated_client()
    response = client.post(
        "/db/img/forward-last",
        data={"prompt": "Analyze this crop"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["analysis"] == "Default analysis"
    assert result["image_id"] == 1

@patch('app.controllers.db.connector.get_con')
def test_forward_last_img_no_images(mock_get_con, authenticated_client):
    """Test cuando no hay imágenes en la base de datos"""
    # Mock database sin resultados
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cur
    mock_get_con.return_value = mock_conn
    
    client = authenticated_client()
    response = client.post(
        "/db/img/forward-last",
        data={"prompt": "Analyze this crop"}
    )
    
    assert response.status_code == 404
    assert response.json()["message"] == "No hay imágenes"

@patch('app.controllers.db.connector.get_con')
def test_forward_last_img_database_error(mock_get_con, authenticated_client):
    """Test cuando hay error en la base de datos"""
    mock_get_con.side_effect = mariadb.Error("Database connection failed")
    
    client = authenticated_client()
    response = client.post(
        "/db/img/forward-last",
        data={"prompt": "Analyze this crop"}
    )
    
    assert response.status_code == 500
    assert "Error BBDD" in response.json()["detail"]

@patch('app.controllers.db.connector.get_con')
@patch('requests.post')
def test_forward_last_img_requests_error(mock_requests_post, mock_get_con, authenticated_client):
    """Test cuando hay error en la petición a requests"""
    # Mock database
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (1, MOCK_IMAGE_BYTES)
    mock_conn.cursor.return_value = mock_cur
    mock_get_con.return_value = mock_conn
    
    # Mock requests error
    mock_requests_post.side_effect = requests.exceptions.RequestException("Connection timeout")
    
    client = authenticated_client()
    response = client.post(
        "/db/img/forward-last",
        data={"prompt": "Analyze this crop"}
    )
    
    assert response.status_code == 503
    assert "Error conectando al análisis" in response.json()["detail"]

@patch('app.controllers.db.connector.get_con')
@patch('requests.post')
def test_forward_last_img_non_200_response(mock_requests_post, mock_get_con, authenticated_client):
    """Test cuando el servicio remoto devuelve error"""
    # Mock database
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (1, MOCK_IMAGE_BYTES)
    mock_conn.cursor.return_value = mock_cur
    mock_get_con.return_value = mock_conn
    
    # Mock requests response con error
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad request"
    mock_requests_post.return_value = mock_response
    
    client = authenticated_client()
    response = client.post(
        "/db/img/forward-last",
        data={"prompt": "Analyze this crop"}
    )
    
    assert response.status_code == 400
    assert "Bad request" in response.json()["detail"]

@patch('app.controllers.db.connector.get_con')
@patch('requests.post')
def test_forward_last_img_text_response(mock_requests_post, mock_get_con, authenticated_client):
    """Test cuando el servicio remoto devuelve texto plano"""
    # Mock database
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (1, MOCK_IMAGE_BYTES)
    mock_conn.cursor.return_value = mock_cur
    mock_get_con.return_value = mock_conn
    
    # Mock requests response con texto
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "Plain text analysis result"
    mock_response.json.side_effect = ValueError("No JSON object")
    mock_response.headers = {"Content-Type": "text/plain"}
    mock_requests_post.return_value = mock_response
    
    client = authenticated_client()
    response = client.post(
        "/db/img/forward-last",
        data={"prompt": "Analyze this crop"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["analysis"] == "Plain text analysis result"

def test_forward_last_img_wrong_token():
    """Test con token de autenticación incorrecto"""
    client = TestClient(app)
    headers = {"Authorization": "Bearer wrong-token"}
    response = client.post(
        "/db/img/forward-last",
        data={"prompt": "Analyze this crop"},
        headers=headers
    )
    
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

# Tests para GET /db/img/last
@patch('app.controllers.db.connector.get_con')
def test_get_last_img_success(mock_get_con, authenticated_client):
    """Test exitoso para obtener última imagen"""
    # Mock database
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (1, MOCK_IMAGE_BYTES)
    mock_conn.cursor.return_value = mock_cur
    mock_get_con.return_value = mock_conn
    
    client = authenticated_client()
    response = client.get("/db/img/last")
    
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == 1
    assert result["image_base64"] == MOCK_IMAGE_BASE64
    assert result["mime_type"] == "image/jpeg"
    
    # Verificar llamadas a DB
    mock_cur.execute.assert_called_once_with("SELECT id, image FROM images ORDER BY id DESC LIMIT 1")
    mock_cur.fetchone.assert_called_once()
    mock_cur.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('app.controllers.db.connector.get_con')
def test_get_last_img_no_images(mock_get_con, authenticated_client):
    """Test cuando no hay imágenes en la base de datos"""
    # Mock database sin resultados
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cur
    mock_get_con.return_value = mock_conn
    
    client = authenticated_client()
    response = client.get("/db/img/last")
    
    assert response.status_code == 404
    assert response.json()["message"] == "No images found"

@patch('app.controllers.db.connector.get_con')
def test_get_last_img_database_error(mock_get_con, authenticated_client):
    """Test cuando hay error en la base de datos"""
    mock_get_con.side_effect = mariadb.Error("Database connection failed")
    
    client = authenticated_client()
    response = client.get("/db/img/last")
    
    assert response.status_code == 500
    assert "Failed to retrieve last image" in response.json()["detail"]

def test_get_last_img_wrong_token():
    """Test con token de autenticación incorrecto"""
    client = TestClient(app)
    headers = {"Authorization": "Bearer wrong-token"}
    response = client.get("/db/img/last", headers=headers)
    
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

# Tests para POST /db/img
@patch('app.controllers.db.connector.get_con')
def test_post_img_success(mock_get_con, authenticated_client):
    """Test exitoso para subir imagen"""
    # Mock database
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.lastrowid = 1
    mock_conn.cursor.return_value = mock_cur
    mock_get_con.return_value = mock_conn
    
    client = authenticated_client()
    
    # Crear archivo de imagen mock
    image_file = io.BytesIO(MOCK_IMAGE_BYTES)
    image_file.name = "test_image.jpg"
    
    response = client.post(
        "/db/img",
        files={"image": ("test_image.jpg", image_file, "image/jpeg")}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == "Image saved successfully"
    assert result["id"] == 1
    
    # Verificar llamadas a DB
    mock_cur.execute.assert_called_once_with(
        "INSERT INTO images (image) VALUES (%s)",
        (MOCK_IMAGE_BYTES,)
    )
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('app.controllers.db.connector.get_con')
def test_post_img_database_error(mock_get_con, authenticated_client):
    """Test cuando hay error en la base de datos al guardar imagen"""
    mock_get_con.side_effect = mariadb.Error("Database connection failed")
    
    client = authenticated_client()
    
    # Crear archivo de imagen mock
    image_file = io.BytesIO(MOCK_IMAGE_BYTES)
    image_file.name = "test_image.jpg"
    
    response = client.post(
        "/db/img",
        files={"image": ("test_image.jpg", image_file, "image/jpeg")}
    )
    
    assert response.status_code == 500
    assert "Error saving image" in response.json()["detail"]



def test_post_img_wrong_token():
    """Test con token de autenticación incorrecto"""
    client = TestClient(app)
    headers = {"Authorization": "Bearer wrong-token"}
    
    image_file = io.BytesIO(MOCK_IMAGE_BYTES)
    image_file.name = "test_image.jpg"
    
    response = client.post(
        "/db/img",
        files={"image": ("test_image.jpg", image_file, "image/jpeg")},
        headers=headers
    )
    
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]



# Tests asíncronos con AsyncClient
@pytest.mark.asyncio
@patch('app.kafka_module.consumer.consume_messages')
async def test_init_kafka_async(mock_consume_messages):
    """Test asíncrono para init_kafka"""
    from httpx import ASGITransport
    
    mock_consume_messages.return_value = None
    
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        response = await ac.get("/db/initkafka", headers=headers)
        assert response.status_code == 200
        assert response.text == "Kafka consumiendo mensajes del topic"
        mock_consume_messages.assert_called_once()

@pytest.mark.asyncio
@patch('app.controllers.db.connector.get_con')
async def test_get_last_img_async(mock_get_con):
    """Test asíncrono para get_last_img"""
    from httpx import ASGITransport
    
    # Mock database
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (1, MOCK_IMAGE_BYTES)
    mock_conn.cursor.return_value = mock_cur
    mock_get_con.return_value = mock_conn
    
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        response = await ac.get("/db/img/last", headers=headers)
        assert response.status_code == 200
        result = response.json()
        assert result["id"] == 1
        assert result["image_base64"] == MOCK_IMAGE_BASE64