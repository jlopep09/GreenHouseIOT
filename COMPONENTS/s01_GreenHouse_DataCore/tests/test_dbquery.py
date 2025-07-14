import pytest
import os
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
import mariadb

# Configurar el token para los tests
TEST_TOKEN = os.getenv("SECRET_TOKEN", "none")

@pytest.fixture
def authenticated_client():
    def _client():
        return TestClient(app, headers={"Authorization": f"Bearer {TEST_TOKEN}"})
    return _client

@pytest.fixture
def mock_db_connection():
    """Mock para la conexión a la base de datos"""
    with patch('app.controllers.db.connector.get_con') as mock_get_con:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_con.return_value = mock_conn
        yield mock_conn, mock_cursor

class TestGetGreenhouseByName:
    
    def test_get_greenhouse_by_name_success(self, mock_db_connection):
        """Test exitoso para obtener invernadero por nombre"""
        mock_conn, mock_cursor = mock_db_connection
        
        # Mock de los datos de retorno
        mock_cursor.description = [('id',), ('name',), ('description',)]
        mock_cursor.fetchall.return_value = [(1, 'test_greenhouse', 'test description')]
        
        from app.controllers.db.db_queries import get_greenhouse_by_name
        
        result = get_greenhouse_by_name("test_greenhouse")
        
        assert result == {"result": [{"id": 1, "name": "test_greenhouse", "description": "test description"}]}
        mock_cursor.execute.assert_called_once_with("SELECT * FROM greenhouses WHERE name=?", ("test_greenhouse",))
        mock_conn.close.assert_called_once()
    
    def test_get_greenhouse_by_name_empty_result(self, mock_db_connection):
        """Test cuando no se encuentra el invernadero"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.description = [('id',), ('name',), ('description',)]
        mock_cursor.fetchall.return_value = []
        
        from app.controllers.db.db_queries import get_greenhouse_by_name
        
        result = get_greenhouse_by_name("nonexistent")
        
        assert result == {"result": []}
        mock_cursor.execute.assert_called_once_with("SELECT * FROM greenhouses WHERE name=?", ("nonexistent",))
        mock_conn.close.assert_called_once()
    
    def test_get_greenhouse_by_name_db_error(self, mock_db_connection):
        """Test cuando hay error de base de datos"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.execute.side_effect = mariadb.Error("Database error")
        
        from app.controllers.db.db_queries import get_greenhouse_by_name
        
        with patch('builtins.print') as mock_print:
            result = get_greenhouse_by_name("test")
            mock_print.assert_called_with("Error retrieving table information: Database error")

class TestGetGreenhouses:
    
    def test_get_greenhouses_success(self, mock_db_connection):
        """Test exitoso para obtener invernaderos de un usuario"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.description = [('id',), ('name',), ('owner_id',)]
        mock_cursor.fetchall.return_value = [(1, 'greenhouse1', 'user123'), (2, 'greenhouse2', 'user123')]
        
        from app.controllers.db.db_queries import get_greenhouses
        
        result = get_greenhouses("user123")
        
        expected = {
            "greenhouses": [
                {"id": 1, "name": "greenhouse1", "owner_id": "user123"},
                {"id": 2, "name": "greenhouse2", "owner_id": "user123"}
            ]
        }
        assert result == expected
        mock_cursor.execute.assert_called_once_with("SELECT * FROM greenhouses WHERE owner_id = ?", ("user123",))
        mock_conn.close.assert_called_once()
    
    def test_get_greenhouses_empty_result(self, mock_db_connection):
        """Test cuando el usuario no tiene invernaderos"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.description = [('id',), ('name',), ('owner_id',)]
        mock_cursor.fetchall.return_value = []
        
        from app.controllers.db.db_queries import get_greenhouses
        
        result = get_greenhouses("user456")
        
        assert result == {"greenhouses": []}
        mock_cursor.execute.assert_called_once_with("SELECT * FROM greenhouses WHERE owner_id = ?", ("user456",))
        mock_conn.close.assert_called_once()
    
    def test_get_greenhouses_db_error(self, mock_db_connection):
        """Test cuando hay error de base de datos"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.execute.side_effect = mariadb.Error("Database error")
        
        from app.controllers.db.db_queries import get_greenhouses
        
        with pytest.raises(HTTPException) as exc_info:
            get_greenhouses("user123")
        
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Failed to retrieve greenhouses"

class TestGetReads:
    
    def test_get_reads_success(self, mock_db_connection):
        """Test exitoso para obtener lecturas de un usuario"""
        mock_conn, mock_cursor = mock_db_connection
        
        # Mock para primera consulta (obtener IDs de invernaderos)
        mock_cursor.fetchall.side_effect = [
            [(1,), (2,)],  # IDs de invernaderos
            [(1, 25.5, 60, 'data1'), (2, 26.0, 65, 'data2')]  # Lecturas
        ]
        mock_cursor.description = [('id',), ('temperature',), ('humidity',), ('data',)]
        
        from app.controllers.db.db_queries import get_reads
        
        with patch('builtins.print'):
            result = get_reads("user123")
        
        expected = {
            "reads": [
                {"id": 1, "temperature": 25.5, "humidity": 60, "data": "data1"},
                {"id": 2, "temperature": 26.0, "humidity": 65, "data": "data2"}
            ]
        }
        assert result == expected
        assert mock_cursor.execute.call_count == 2
        mock_conn.close.assert_called_once()
    
    def test_get_reads_no_greenhouses(self, mock_db_connection):
        """Test cuando el usuario no tiene invernaderos"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.fetchall.return_value = []  # No hay invernaderos
        
        from app.controllers.db.db_queries import get_reads
        
        with patch('builtins.print'):
            result = get_reads("user456")
        
        assert result == {"reads": []}
        mock_cursor.execute.assert_called_once_with("SELECT id FROM greenhouses WHERE owner_id = ?", ("user456",))
        mock_conn.close.assert_called_once()
    
    def test_get_reads_db_error(self, mock_db_connection):
        """Test cuando hay error de base de datos"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.execute.side_effect = mariadb.Error("Database error")
        
        from app.controllers.db.db_queries import get_reads
        
        with pytest.raises(HTTPException) as exc_info:
            with patch('builtins.print'):
                get_reads("user123")
        
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Failed to retrieve reads"

class TestGetReadsByID:
    
    def test_get_reads_byid_success(self, mock_db_connection):
        """Test exitoso para obtener lecturas por ID de invernadero"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.description = [('id',), ('temperature',), ('humidity',)]
        mock_cursor.fetchall.return_value = [(1, 25.5, 60), (2, 26.0, 65)]
        
        from app.controllers.db.db_queries import get_reads_byid
        
        result = get_reads_byid(1)
        
        expected = {
            "reads": [
                {"id": 1, "temperature": 25.5, "humidity": 60},
                {"id": 2, "temperature": 26.0, "humidity": 65}
            ]
        }
        assert result == expected
        mock_cursor.execute.assert_called_once_with("SELECT * FROM sensor_reads WHERE gh_id=?", (1,))
        mock_conn.close.assert_called_once()
    
    def test_get_reads_byid_empty_result(self, mock_db_connection):
        """Test cuando no hay lecturas para el invernadero"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.description = [('id',), ('temperature',), ('humidity',)]
        mock_cursor.fetchall.return_value = []
        
        from app.controllers.db.db_queries import get_reads_byid
        
        result = get_reads_byid(999)
        
        assert result == {"reads": []}
        mock_cursor.execute.assert_called_once_with("SELECT * FROM sensor_reads WHERE gh_id=?", (999,))
        mock_conn.close.assert_called_once()
    
    def test_get_reads_byid_db_error(self, mock_db_connection):
        """Test cuando hay error de base de datos"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.execute.side_effect = mariadb.Error("Database error")
        
        from app.controllers.db.db_queries import get_reads_byid
        
        with patch('builtins.print') as mock_print:
            result = get_reads_byid(1)
            mock_print.assert_called_with("Error retrieving table information: Database error")

class TestGetGreenhouse:
    
    def test_get_greenhouse_success(self, mock_db_connection):
        """Test exitoso para obtener invernadero por ID"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.fetchall.return_value = [(1, 'greenhouse1', 'description1', 'image1')]
        
        from app.controllers.db.db_queries import get_greenhouse
        
        result = get_greenhouse(1)
        
        expected = "1 | greenhouse1 | description1 | image1\n"
        assert result == expected
        mock_cursor.execute.assert_called_once_with("SELECT * FROM greenhouses WHERE id=?", (1,))
        mock_conn.close.assert_called_once()
    
    def test_get_greenhouse_empty_result(self, mock_db_connection):
        """Test cuando no se encuentra el invernadero"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.fetchall.return_value = []
        
        from app.controllers.db.db_queries import get_greenhouse
        
        result = get_greenhouse(999)
        
        assert result == ""
        mock_cursor.execute.assert_called_once_with("SELECT * FROM greenhouses WHERE id=?", (999,))
        mock_conn.close.assert_called_once()
    
    def test_get_greenhouse_db_error(self, mock_db_connection):
        """Test cuando hay error de base de datos"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.execute.side_effect = mariadb.Error("Database error")
        
        from app.controllers.db.db_queries import get_greenhouse
        
        with patch('builtins.print') as mock_print:
            result = get_greenhouse(1)
            mock_print.assert_called_with("Error retrieving table information: Database error")

class TestCreateGreenhouse:
    
    def test_create_greenhouse_success(self, mock_db_connection):
        """Test exitoso para crear invernadero"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.lastrowid = 123
        
        from app.controllers.db.db_queries import create_greenhouse
        
        result = create_greenhouse("test_gh", "192.168.1.1", "ABC123", "test description", b"image_data")
        
        expected = {"message": "Greenhouse created successfully", "id": 123}
        assert result == expected
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO greenhouses (name, description, image, ip, sync_code) VALUES (?, ?, ?, ?, ?)",
            ("test_gh", "test description", b"image_data", "192.168.1.1", "ABC123")
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
    
    def test_create_greenhouse_minimal_params(self, mock_db_connection):
        """Test crear invernadero con parámetros mínimos"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.lastrowid = 124
        
        from app.controllers.db.db_queries import create_greenhouse
        
        result = create_greenhouse("test_gh", "192.168.1.1", "ABC123")
        
        expected = {"message": "Greenhouse created successfully", "id": 124}
        assert result == expected
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO greenhouses (name, description, image, ip, sync_code) VALUES (?, ?, ?, ?, ?)",
            ("test_gh", None, None, "192.168.1.1", "ABC123")
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
    
    def test_create_greenhouse_db_error(self, mock_db_connection):
        """Test cuando hay error de base de datos"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.execute.side_effect = mariadb.Error("Database error")
        
        from app.controllers.db.db_queries import create_greenhouse
        
        with pytest.raises(HTTPException) as exc_info:
            create_greenhouse("test_gh", "192.168.1.1", "ABC123")
        
        assert exc_info.value.status_code == 500
        assert "Error creating greenhouse: Database error" in str(exc_info.value.detail)

class TestSyncGreenhouse:
    
    def test_sync_greenhouse_success(self, mock_db_connection):
        """Test exitoso para sincronizar invernadero"""
        mock_conn, mock_cursor = mock_db_connection
        
        # Mock para consulta SELECT
        mock_cursor.fetchone.return_value = (1, "ABC123", None)  # ID, sync_code, owner_id
        
        from app.controllers.db.db_queries import sync_greenhouse
        
        result = sync_greenhouse("test_gh", "ABC123", "user123")
        
        expected = {"message": "Greenhouse updated successfully", "name": "test_gh"}
        assert result == expected
        
        # Verificar llamadas
        assert mock_cursor.execute.call_count == 2
        mock_cursor.execute.assert_any_call("SELECT id, sync_code, owner_id FROM greenhouses WHERE name = ?", ("test_gh",))
        mock_cursor.execute.assert_any_call(
            "\n            UPDATE greenhouses\n            SET owner_id = ?\n            WHERE name = ?\n            ",
            ("user123", "test_gh")
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
    
    def test_sync_greenhouse_not_found(self, mock_db_connection):
        """Test cuando el invernadero no existe"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.fetchone.return_value = None
        
        from app.controllers.db.db_queries import sync_greenhouse
        
        with pytest.raises(HTTPException) as exc_info:
            sync_greenhouse("nonexistent", "ABC123", "user123")
        
        assert exc_info.value.status_code == 404
        assert "Greenhouse with name 'nonexistent' not found" in str(exc_info.value.detail)
    
    def test_sync_greenhouse_already_synced(self, mock_db_connection):
        """Test cuando el invernadero ya está sincronizado"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.fetchone.return_value = (1, "ABC123", "existing_user")
        
        from app.controllers.db.db_queries import sync_greenhouse
        
        with pytest.raises(HTTPException) as exc_info:
            sync_greenhouse("test_gh", "ABC123", "user123")
        
        assert exc_info.value.status_code == 400
        assert "Greenhouse already synced" in str(exc_info.value.detail)
    
    def test_sync_greenhouse_invalid_code(self, mock_db_connection):
        """Test cuando el código de sincronización es inválido"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.fetchone.return_value = (1, "ABC123", None)
        
        from app.controllers.db.db_queries import sync_greenhouse
        
        with pytest.raises(HTTPException) as exc_info:
            sync_greenhouse("test_gh", "WRONG_CODE", "user123")
        
        assert exc_info.value.status_code == 409
        assert "Greenhouse sync code is not valid" in str(exc_info.value.detail)

class TestUpdateGreenhouseIP:
    
    def test_update_greenhouse_ip_success(self, mock_db_connection):
        """Test exitoso para actualizar IP de invernadero"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.fetchone.return_value = (1,)  # ID del invernadero
        
        from app.controllers.db.db_queries import update_greenhouse_ip
        
        result = update_greenhouse_ip("test_gh", "192.168.1.100")
        
        expected = {"message": "Greenhouse updated successfully", "name": "test_gh"}
        assert result == expected
        
        # Verificar llamadas
        assert mock_cursor.execute.call_count == 2
        mock_cursor.execute.assert_any_call("SELECT id FROM greenhouses WHERE name = ?", ("test_gh",))
        mock_cursor.execute.assert_any_call(
            "\n            UPDATE greenhouses\n            SET ip = ?\n            WHERE name = ?\n            ",
            ("192.168.1.100", "test_gh")
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
    
    def test_update_greenhouse_ip_not_found(self, mock_db_connection):
        """Test cuando el invernadero no existe"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.fetchone.return_value = None
        
        from app.controllers.db.db_queries import update_greenhouse_ip
        
        with pytest.raises(HTTPException) as exc_info:
            update_greenhouse_ip("nonexistent", "192.168.1.100")
        
        assert exc_info.value.status_code == 404
        assert "Greenhouse with name 'nonexistent' not found" in str(exc_info.value.detail)
    
    def test_update_greenhouse_ip_db_error(self, mock_db_connection):
        """Test cuando hay error de base de datos"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.execute.side_effect = mariadb.Error("Database error")
        
        from app.controllers.db.db_queries import update_greenhouse_ip
        
        with pytest.raises(HTTPException) as exc_info:
            update_greenhouse_ip("test_gh", "192.168.1.100")
        
        assert exc_info.value.status_code == 500
        assert "Error updating greenhouse: Database error" in str(exc_info.value.detail)

class TestCreateRead:
    
    @patch('app.controllers.db.db_queries.const.WATER_MIN_RANGE', 0)
    @patch('app.controllers.db.db_queries.const.WATER_MAX_RANGE', 1000)
    def test_create_read_success(self, mock_db_connection):
        """Test exitoso para crear lectura"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.lastrowid = 456
        
        from app.controllers.db.db_queries import create_read
        
        result = create_read(1500, 60, 500, 25, True, 22.5, 1)
        
        expected = {"message": "Read created successfully", "id": 456}
        assert result == expected
        
        # Verificar que se llamó con los parámetros correctos (incluyendo conversión de water_level)
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert args[0] == "INSERT INTO sensor_reads (tds, humidity, water_level, temperature, light_level, water_temperature, gh_id) VALUES (?, ?, ?, ?, ?, ?,?)"
        assert args[1][0] == 1500  # tds
        assert args[1][1] == 60    # humidity
        assert args[1][2] == 50    # water_level convertido a porcentaje inverso
        assert args[1][3] == 25    # temperature
        assert args[1][4] == True  # light_level
        assert args[1][5] == 22.5  # water_temperature
        assert args[1][6] == 1     # gh_id
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
    
    @patch('app.controllers.db.db_queries.const.WATER_MIN_RANGE', 0)
    @patch('app.controllers.db.db_queries.const.WATER_MAX_RANGE', 1000)
    def test_create_read_tds_too_high(self, mock_db_connection):
        """Test cuando TDS es demasiado alto"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.lastrowid = 457
        
        from app.controllers.db.db_queries import create_read
        
        with patch('builtins.print') as mock_print:
            result = create_read(3000, 60, 500, 25, True, 22.5, 1)
        
        expected = {"message": "Read created successfully", "id": 457}
        assert result == expected
        
        # Verificar que se imprimió el mensaje de error
        mock_print.assert_called_with("Tds no valido, valor demasiado alto ", 3000)
        
        # Verificar que TDS se guardó como 0
        args = mock_cursor.execute.call_args[0]
        assert args[1][0] == 0  # tds corregido a 0
    
    def test_create_read_db_error(self, mock_db_connection):
        """Test cuando hay error de base de datos"""
        mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.execute.side_effect = mariadb.Error("Database error")
        
        from app.controllers.db.db_queries import create_read
        
        with pytest.raises(HTTPException) as exc_info:
            create_read(1500, 60, 500, 25, True, 22.5, 1)
        
        assert exc_info.value.status_code == 500
        assert "Error creating read: Database error" in str(exc_info.value.detail)

class TestUtilityFunctions:
    
    def test_get_percentage(self):
        """Test función get_percentage"""
        from app.controllers.db.db_queries import get_percentage
        
        # Test valores normales
        assert get_percentage(50, 0, 100) == 50
        assert get_percentage(0, 0, 100) == 0
        assert get_percentage(100, 0, 100) == 100
        
        # Test con rango diferente
        assert get_percentage(500, 0, 1000) == 50
        assert get_percentage(250, 0, 1000) == 25
    
    def test_get_percentage_inverse(self):
        """Test función get_percentage_inverse"""
        from app.controllers.db.db_queries import get_percentage_inverse
        
        # Test valores normales
        assert get_percentage_inverse(50, 0, 100) == 50  # 100 - 50 = 50
        assert get_percentage_inverse(0, 0, 100) == 100  # 100 - 0 = 100
        assert get_percentage_inverse(100, 0, 100) == 0  # 100 - 100 = 0
        
        # Test con rango diferente
        assert get_percentage_inverse(500, 0, 1000) == 50  # 100 - 50 = 50
        assert get_percentage_inverse(250, 0, 1000) == 75  # 100 - 25 = 75