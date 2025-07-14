import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
import mariadb

# Importar las funciones a testear
from app.controllers.db.connector import (
    get_greenhouse_by_name,
    get_greenhouses,
    get_reads,
    get_reads_byid,
    get_greenhouse,
    create_greenhouse,
    sync_greenhouse,
    update_greenhouse_ip,
    create_read,
    get_percentage,
    get_percentage_inverse
)

TEST_TOKEN = os.getenv("SECRET_TOKEN", "none")

class TestGetGreenhouseByName:
    
    @patch('app.controllers.db.connector.connector.get_con')
    def test_get_greenhouse_by_name_success(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        # Mock de la descripción de columnas
        mock_cur.description = [('id',), ('name',), ('description',)]
        mock_cur.fetchall.return_value = [
            (1, 'greenhouse1', 'Test greenhouse'),
            (2, 'greenhouse2', 'Another greenhouse')
        ]
        
        # Ejecutar función
        result = get_greenhouse_by_name("greenhouse1")
        
        # Verificaciones
        mock_cur.execute.assert_called_once_with("SELECT * FROM greenhouses WHERE name=?", ("greenhouse1",))
        mock_conn.close.assert_called_once()
        assert result == {"result": [
            {'id': 1, 'name': 'greenhouse1', 'description': 'Test greenhouse'},
            {'id': 2, 'name': 'greenhouse2', 'description': 'Another greenhouse'}
        ]}

    @patch('app.controllers.db.connector.connector.get_con')
    def test_get_greenhouse_by_name_empty_result(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        mock_cur.description = [('id',), ('name',), ('description',)]
        mock_cur.fetchall.return_value = []
        
        # Ejecutar función
        result = get_greenhouse_by_name("nonexistent")
        
        # Verificaciones
        assert result == {"result": []}
        mock_conn.close.assert_called_once()

    @patch('app.controllers.db.connector.connector.get_con')
    @patch('builtins.print')
    def test_get_greenhouse_by_name_db_error(self, mock_print, mock_get_con):
        # Configurar mock para lanzar excepción
        mock_get_con.side_effect = mariadb.Error("Database connection failed")
        
        # Ejecutar función
        result = get_greenhouse_by_name("greenhouse1")
        
        # Verificaciones
        mock_print.assert_called_once_with("Error retrieving table information: Database connection failed")
        assert result is None


class TestGetGreenhouses:
    
    @patch('app.controllers.db.connector.connector.get_con')
    def test_get_greenhouses_success(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        mock_cur.description = [('id',), ('name',), ('owner_id',)]
        mock_cur.fetchall.return_value = [
            (1, 'greenhouse1', 'user123'),
            (2, 'greenhouse2', 'user123')
        ]
        
        # Ejecutar función
        result = get_greenhouses("user123")
        
        # Verificaciones
        mock_cur.execute.assert_called_once_with("SELECT * FROM greenhouses WHERE owner_id = ?", ("user123",))
        mock_conn.close.assert_called_once()
        assert result == {"greenhouses": [
            {'id': 1, 'name': 'greenhouse1', 'owner_id': 'user123'},
            {'id': 2, 'name': 'greenhouse2', 'owner_id': 'user123'}
        ]}

    @patch('app.controllers.db.connector.connector.get_con')
    def test_get_greenhouses_db_error(self, mock_get_con):
        # Configurar mock para lanzar excepción
        mock_get_con.side_effect = mariadb.Error("Database connection failed")
        
        # Ejecutar función y verificar que lanza HTTPException
        with pytest.raises(HTTPException) as exc_info:
            get_greenhouses("user123")
        
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Failed to retrieve greenhouses"


class TestGetReads:
    
    @patch('app.controllers.db.connector.connector.get_con')
    @patch('builtins.print')
    def test_get_reads_success(self, mock_print, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        # Mock para obtener IDs de invernaderos
        mock_cur.fetchall.side_effect = [
            [(1,), (2,)],  # IDs de invernaderos
            [(1, 25.5, 60, 80, True, 22.0, 1), (2, 30.0, 70, 85, False, 24.0, 2)]  # Lecturas
        ]
        
        # Mock para descripción de columnas de sensor_reads
        mock_cur.description = [('id',), ('tds',), ('humidity',), ('water_level',), ('light_level',), ('water_temperature',), ('gh_id',)]
        
        # Ejecutar función
        result = get_reads("user123")
        
        # Verificaciones
        assert mock_cur.execute.call_count == 2
        mock_conn.close.assert_called_once()
        assert len(result["reads"]) == 2

    @patch('app.controllers.db.connector.connector.get_con')
    @patch('builtins.print')
    def test_get_reads_no_greenhouses(self, mock_print, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        # Mock para obtener IDs vacíos
        mock_cur.fetchall.return_value = []
        
        # Ejecutar función
        result = get_reads("user123")
        
        # Verificaciones
        mock_conn.close.assert_called_once()
        assert result == {"reads": []}

    @patch('app.controllers.db.connector.connector.get_con')
    @patch('builtins.print')
    def test_get_reads_db_error(self, mock_print, mock_get_con):
        # Configurar mock para lanzar excepción
        mock_get_con.side_effect = mariadb.Error("Database connection failed")
        
        # Ejecutar función y verificar que lanza HTTPException
        with pytest.raises(HTTPException) as exc_info:
            get_reads("user123")
        
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Failed to retrieve reads"


class TestGetReadsByID:
    
    @patch('app.controllers.db.connector.connector.get_con')
    def test_get_reads_byid_success(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        mock_cur.description = [('id',), ('tds',), ('humidity',), ('gh_id',)]
        mock_cur.fetchall.return_value = [
            (1, 25.5, 60, 1),
            (2, 30.0, 70, 1)
        ]
        
        # Ejecutar función
        result = get_reads_byid(1)
        
        # Verificaciones
        mock_cur.execute.assert_called_once_with("SELECT * FROM sensor_reads WHERE gh_id=?", (1,))
        mock_conn.close.assert_called_once()
        assert len(result["reads"]) == 2

    @patch('app.controllers.db.connector.connector.get_con')
    @patch('builtins.print')
    def test_get_reads_byid_db_error(self, mock_print, mock_get_con):
        # Configurar mock para lanzar excepción
        mock_get_con.side_effect = mariadb.Error("Database connection failed")
        
        # Ejecutar función
        result = get_reads_byid(1)
        
        # Verificaciones
        mock_print.assert_called_once_with("Error retrieving table information: Database connection failed")
        assert result is None


class TestGetGreenhouse:
    
    @patch('app.controllers.db.connector.connector.get_con')
    def test_get_greenhouse_success(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        mock_cur.fetchall.return_value = [
            (1, '2023-01-01', 'greenhouse1', 'Test greenhouse', 'image.jpg')
        ]
        
        # Ejecutar función
        result = get_greenhouse(1)
        
        # Verificaciones
        mock_cur.execute.assert_called_once_with("SELECT * FROM greenhouses WHERE id=?", (1,))
        mock_conn.close.assert_called_once()
        assert "1 | 2023-01-01 | greenhouse1 | Test greenhouse | image.jpg" in result

    @patch('app.controllers.db.connector.connector.get_con')
    @patch('builtins.print')
    def test_get_greenhouse_db_error(self, mock_print, mock_get_con):
        # Configurar mock para lanzar excepción
        mock_get_con.side_effect = mariadb.Error("Database connection failed")
        
        # Ejecutar función
        result = get_greenhouse(1)
        
        # Verificaciones
        mock_print.assert_called_once_with("Error retrieving table information: Database connection failed")
        assert result is None


class TestCreateGreenhouse:
    
    @patch('app.controllers.db.connector.connector.get_con')
    def test_create_greenhouse_success(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.lastrowid = 123
        
        # Ejecutar función
        result = create_greenhouse("test_greenhouse", "192.168.1.100", "sync123", "Test description", b"image_data")
        
        # Verificaciones
        mock_cur.execute.assert_called_once_with(
            "INSERT INTO greenhouses (name, description, image, ip, sync_code) VALUES (?, ?, ?, ?, ?)",
            ("test_greenhouse", "Test description", b"image_data", "192.168.1.100", "sync123")
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        assert result == {"message": "Greenhouse created successfully", "id": 123}

    @patch('app.controllers.db.connector.connector.get_con')
    def test_create_greenhouse_db_error(self, mock_get_con):
        # Configurar mock para lanzar excepción
        mock_get_con.side_effect = mariadb.Error("Database connection failed")
        
        # Ejecutar función y verificar que lanza HTTPException
        with pytest.raises(HTTPException) as exc_info:
            create_greenhouse("test_greenhouse", "192.168.1.100", "sync123")
        
        assert exc_info.value.status_code == 500
        assert "Error creating greenhouse" in exc_info.value.detail


class TestSyncGreenhouse:
    
    @patch('app.controllers.db.connector.connector.get_con')
    def test_sync_greenhouse_success(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        # Mock para encontrar invernadero sin owner
        mock_cur.fetchone.return_value = (1, "sync123", None)
        
        # Ejecutar función
        result = sync_greenhouse("test_greenhouse", "sync123", "user123")
        
        # Verificaciones
        assert mock_cur.execute.call_count == 2
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        assert result == {"message": "Greenhouse updated successfully", "name": "test_greenhouse"}

    @patch('app.controllers.db.connector.connector.get_con')
    def test_sync_greenhouse_not_found(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        # Mock para no encontrar invernadero
        mock_cur.fetchone.return_value = None
        
        # Ejecutar función y verificar que lanza HTTPException
        with pytest.raises(HTTPException) as exc_info:
            sync_greenhouse("nonexistent", "sync123", "user123")
        
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail

    @patch('app.controllers.db.connector.connector.get_con')
    def test_sync_greenhouse_already_synced(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        # Mock para invernadero ya sincronizado
        mock_cur.fetchone.return_value = (1, "sync123", "existing_user")
        
        # Ejecutar función y verificar que lanza HTTPException
        with pytest.raises(HTTPException) as exc_info:
            sync_greenhouse("test_greenhouse", "sync123", "user123")
        
        assert exc_info.value.status_code == 400
        assert "already synced" in exc_info.value.detail

    @patch('app.controllers.db.connector.connector.get_con')
    def test_sync_greenhouse_invalid_code(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        # Mock para código de sincronización inválido
        mock_cur.fetchone.return_value = (1, "different_sync", None)
        
        # Ejecutar función y verificar que lanza HTTPException
        with pytest.raises(HTTPException) as exc_info:
            sync_greenhouse("test_greenhouse", "sync123", "user123")
        
        assert exc_info.value.status_code == 409
        assert "not valid" in exc_info.value.detail


class TestUpdateGreenhouseIP:
    
    @patch('app.controllers.db.connector.connector.get_con')
    def test_update_greenhouse_ip_success(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        # Mock para encontrar invernadero
        mock_cur.fetchone.return_value = (1,)
        
        # Ejecutar función
        result = update_greenhouse_ip("test_greenhouse", "192.168.1.200")
        
        # Verificaciones
        assert mock_cur.execute.call_count == 2
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        assert result == {"message": "Greenhouse updated successfully", "name": "test_greenhouse"}

    @patch('app.controllers.db.connector.connector.get_con')
    def test_update_greenhouse_ip_not_found(self, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        # Mock para no encontrar invernadero
        mock_cur.fetchone.return_value = None
        
        # Ejecutar función y verificar que lanza HTTPException
        with pytest.raises(HTTPException) as exc_info:
            update_greenhouse_ip("nonexistent", "192.168.1.200")
        
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail

    @patch('app.controllers.db.connector.connector.get_con')
    def test_update_greenhouse_ip_db_error(self, mock_get_con):
        # Configurar mock para lanzar excepción
        mock_get_con.side_effect = mariadb.Error("Database connection failed")
        
        # Ejecutar función y verificar que lanza HTTPException
        with pytest.raises(HTTPException) as exc_info:
            update_greenhouse_ip("test_greenhouse", "192.168.1.200")
        
        assert exc_info.value.status_code == 500
        assert "Error updating greenhouse" in exc_info.value.detail


class TestCreateRead:
    
    @patch('app.controllers.db.connector.connector.get_con')
    @patch('app.controllers.db.connector.get_percentage_inverse')
    def test_create_read_success(self, mock_get_percentage_inverse, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.lastrowid = 456
        mock_get_percentage_inverse.return_value = 75
        
        # Ejecutar función
        result = create_read(1500, 60, 800, 25, True, 22.5, 1)
        
        # Verificaciones
        mock_cur.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        assert result == {"message": "Read created successfully", "id": 456}

    @patch('app.controllers.db.connector.connector.get_con')
    @patch('app.controllers.db.connector.get_percentage_inverse')
    @patch('builtins.print')
    def test_create_read_high_tds(self, mock_print, mock_get_percentage_inverse, mock_get_con):
        # Configurar mocks
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.lastrowid = 456
        mock_get_percentage_inverse.return_value = 75
        
        # Ejecutar función con TDS alto
        result = create_read(2500, 60, 800, 25, True, 22.5, 1)
        
        # Verificaciones
        mock_print.assert_called_once_with("Tds no valido, valor demasiado alto ", 2500)
        # Verificar que se insertó con tds=0
        args, kwargs = mock_cur.execute.call_args
        assert args[1][0] == 0  # TDS debe ser 0

    @patch('app.controllers.db.connector.connector.get_con')
    def test_create_read_db_error(self, mock_get_con):
        # Configurar mock para lanzar excepción
        mock_get_con.side_effect = mariadb.Error("Database connection failed")
        
        # Ejecutar función y verificar que lanza HTTPException
        with pytest.raises(HTTPException) as exc_info:
            create_read(1500, 60, 800, 25, True, 22.5, 1)
        
        assert exc_info.value.status_code == 500
        assert "Error creating read" in exc_info.value.detail


class TestUtilityFunctions:
    
    def test_get_percentage_normal_range(self):
        # Test con valores normales
        result = get_percentage(50, 0, 100)
        assert result == 50
        
        result = get_percentage(25, 0, 100)
        assert result == 25

    def test_get_percentage_edge_cases(self):
        # Test con valores en los extremos
        result = get_percentage(0, 0, 100)
        assert result == 0
        
        result = get_percentage(100, 0, 100)
        assert result == 100

    def test_get_percentage_different_ranges(self):
        # Test con rangos diferentes
        result = get_percentage(500, 0, 1000)
        assert result == 50

    def test_get_percentage_inverse_normal_range(self):
        # Test con valores normales
        result = get_percentage_inverse(50, 0, 100)
        assert result == 50  # 100 - 50 = 50
        
        result = get_percentage_inverse(25, 0, 100)
        assert result == 75  # 100 - 25 = 75

    def test_get_percentage_inverse_edge_cases(self):
        # Test con valores en los extremos
        result = get_percentage_inverse(0, 0, 100)
        assert result == 100  # 100 - 0 = 100
        
        result = get_percentage_inverse(100, 0, 100)
        assert result == 0  # 100 - 100 = 0

    def test_get_percentage_inverse_different_ranges(self):
        # Test con rangos diferentes
        result = get_percentage_inverse(500, 0, 1000)
        assert result == 50  # 100 - 50 = 50


# Fixtures para facilitar tests
@pytest.fixture
def mock_db_connection():
    with patch('app.controllers.db.connector.connector.get_con') as mock_get_con:
        mock_conn = Mock()
        mock_cur = Mock()
        mock_get_con.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        yield mock_conn, mock_cur


@pytest.fixture
def sample_greenhouse_data():
    return {
        'id': 1,
        'name': 'test_greenhouse',
        'description': 'Test greenhouse',
        'ip': '192.168.1.100',
        'sync_code': 'sync123',
        'owner_id': 'user123'
    }


@pytest.fixture
def sample_read_data():
    return {
        'id': 1,
        'tds': 1500,
        'humidity': 60,
        'water_level': 800,
        'temperature': 25,
        'light_level': True,
        'water_temperature': 22.5,
        'gh_id': 1
    }