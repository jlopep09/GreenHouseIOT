import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException, status
import mariadb
from app.controllers.db.connector import get_con

# Configurar el token para los tests
TEST_TOKEN = os.getenv("SECRET_TOKEN", "none")

class TestDatabaseConnector:
    """Test suite para el módulo connector de base de datos"""
    
    def setup_method(self):
        """Setup antes de cada test"""
        self.valid_env_vars = {
            "DB_USER": "test_user",
            "DB_PASSWORD": "test_password", 
            "DB_HOST": "localhost",
            "DB_PORT": "3306",
            "DB_NAME": "test_db"
        }
        
        self.mock_connection = Mock()

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost", 
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
    })
    def test_get_con_success(self, mock_load_dotenv, mock_connect):
        """Test conexión exitosa a la base de datos"""
        mock_connect.return_value = self.mock_connection
        
        result = get_con()
        
        # Verificar que load_dotenv fue llamado
        mock_load_dotenv.assert_called_once()
        
        # Verificar que mariadb.connect fue llamado con los parámetros correctos
        mock_connect.assert_called_once_with(
            user="test_user",
            password="test_password",
            host="localhost",
            port=3306,
            database="test_db"
        )
        
        assert result == self.mock_connection

    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {}, clear=True)
    def test_get_con_missing_all_env_vars(self, mock_load_dotenv):
        """Test cuando faltan todas las variables de entorno"""
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_412_PRECONDITION_FAILED
        assert exc_info.value.detail == "Missing one or more required environment variables"
        mock_load_dotenv.assert_called_once()

    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "3306"
        # Falta DB_NAME
    })
    def test_get_con_missing_db_name(self, mock_load_dotenv):
        """Test cuando falta la variable DB_NAME"""
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_412_PRECONDITION_FAILED
        assert exc_info.value.detail == "Missing one or more required environment variables"

    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_NAME": "test_db"
        # Falta DB_PORT
    })
    def test_get_con_missing_db_port(self, mock_load_dotenv):
        """Test cuando falta la variable DB_PORT"""
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_412_PRECONDITION_FAILED
        assert exc_info.value.detail == "Missing one or more required environment variables"

    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
        # Falta DB_USER
    })
    def test_get_con_missing_db_user(self, mock_load_dotenv):
        """Test cuando falta la variable DB_USER"""
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_412_PRECONDITION_FAILED
        assert exc_info.value.detail == "Missing one or more required environment variables"

    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
        # Falta DB_PASSWORD
    })
    def test_get_con_missing_db_password(self, mock_load_dotenv):
        """Test cuando falta la variable DB_PASSWORD"""
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_412_PRECONDITION_FAILED
        assert exc_info.value.detail == "Missing one or more required environment variables"

    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
        # Falta DB_HOST
    })
    def test_get_con_missing_db_host(self, mock_load_dotenv):
        """Test cuando falta la variable DB_HOST"""
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_412_PRECONDITION_FAILED
        assert exc_info.value.detail == "Missing one or more required environment variables"

    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
    })
    def test_get_con_empty_db_user(self, mock_load_dotenv):
        """Test cuando DB_USER está vacío"""
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_412_PRECONDITION_FAILED
        assert exc_info.value.detail == "Missing one or more required environment variables"

    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
    })
    def test_get_con_empty_db_password(self, mock_load_dotenv):
        """Test cuando DB_PASSWORD está vacío"""
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_412_PRECONDITION_FAILED
        assert exc_info.value.detail == "Missing one or more required environment variables"

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "",  # Puerto vacío
        "DB_NAME": "test_db"
    })
    def test_get_con_empty_db_port_uses_default(self, mock_load_dotenv, mock_connect):
        """Test cuando DB_PORT está vacío usa el puerto por defecto 3306"""
        mock_connect.return_value = self.mock_connection
        
        result = get_con()
        
        # Verificar que se usa el puerto por defecto 3306
        mock_connect.assert_called_once_with(
            user="test_user",
            password="test_password", 
            host="localhost",
            port=3306,  # Puerto por defecto
            database="test_db"
        )
        
        assert result == self.mock_connection

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "3307",  # Puerto personalizado
        "DB_NAME": "test_db"
    })
    def test_get_con_custom_port(self, mock_load_dotenv, mock_connect):
        """Test con puerto personalizado"""
        mock_connect.return_value = self.mock_connection
        
        result = get_con()
        
        # Verificar que se usa el puerto personalizado
        mock_connect.assert_called_once_with(
            user="test_user",
            password="test_password",
            host="localhost", 
            port=3307,  # Puerto personalizado
            database="test_db"
        )
        
        assert result == self.mock_connection

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "invalid_port",  # Puerto inválido
        "DB_NAME": "test_db"
    })
    def test_get_con_invalid_port_format(self, mock_load_dotenv, mock_connect):
        """Test con formato de puerto inválido"""
        # int() lanzará ValueError que debería ser capturado
        with pytest.raises(ValueError):
            get_con()

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
    })
    def test_get_con_mariadb_connection_error(self, mock_load_dotenv, mock_connect):
        """Test cuando mariadb.connect lanza un error"""
        mock_connect.side_effect = mariadb.Error("Connection failed")
        
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Error connecting to MariaDB Platform: Connection failed" in exc_info.value.detail

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
    })
    def test_get_con_mariadb_authentication_error(self, mock_load_dotenv, mock_connect):
        """Test cuando falla la autenticación con MariaDB"""
        mock_connect.side_effect = mariadb.Error("Access denied for user")
        
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Error connecting to MariaDB Platform: Access denied for user" in exc_info.value.detail

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
    })
    def test_get_con_mariadb_host_unreachable(self, mock_load_dotenv, mock_connect):
        """Test cuando el host de MariaDB no es alcanzable"""
        mock_connect.side_effect = mariadb.Error("Can't connect to MySQL server")
        
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Error connecting to MariaDB Platform: Can't connect to MySQL server" in exc_info.value.detail

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "nonexistent_db"
    })
    def test_get_con_mariadb_database_not_found(self, mock_load_dotenv, mock_connect):
        """Test cuando la base de datos no existe"""
        mock_connect.side_effect = mariadb.Error("Unknown database 'nonexistent_db'")
        
        with pytest.raises(HTTPException) as exc_info:
            get_con()
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Error connecting to MariaDB Platform: Unknown database 'nonexistent_db'" in exc_info.value.detail

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
    })
    def test_get_con_load_dotenv_called_first(self, mock_load_dotenv, mock_connect):
        """Test que load_dotenv se llama antes de obtener variables de entorno"""
        mock_connect.return_value = self.mock_connection
        
        # Crear un mock que verifique el orden de llamadas
        call_order = []
        
        def track_load_dotenv():
            call_order.append('load_dotenv')
            
        def track_connect(*args, **kwargs):
            call_order.append('connect')
            return self.mock_connection
        
        mock_load_dotenv.side_effect = track_load_dotenv
        mock_connect.side_effect = track_connect
        
        get_con()
        
        # Verificar que load_dotenv se llamó antes que connect
        assert call_order == ['load_dotenv', 'connect']

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "0",  # Puerto 0
        "DB_NAME": "test_db"
    })
    def test_get_con_port_zero(self, mock_load_dotenv, mock_connect):
        """Test con puerto 0"""
        mock_connect.return_value = self.mock_connection
        
        result = get_con()
        
        # Verificar que se convierte el puerto a int
        mock_connect.assert_called_once_with(
            user="test_user",
            password="test_password",
            host="localhost",
            port=0,
            database="test_db"
        )
        
        assert result == self.mock_connection

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "65535",  # Puerto máximo
        "DB_NAME": "test_db"
    })
    def test_get_con_max_port(self, mock_load_dotenv, mock_connect):
        """Test con puerto máximo válido"""
        mock_connect.return_value = self.mock_connection
        
        result = get_con()
        
        mock_connect.assert_called_once_with(
            user="test_user",
            password="test_password",
            host="localhost",
            port=65535,
            database="test_db"
        )
        
        assert result == self.mock_connection

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
    })
    def test_get_con_returns_connection_object(self, mock_load_dotenv, mock_connect):
        """Test que get_con retorna el objeto de conexión correcto"""
        mock_connect.return_value = self.mock_connection
        
        result = get_con()
        
        # Verificar que el resultado es exactamente el objeto de conexión mockeado
        assert result is self.mock_connection
        assert result == self.mock_connection

    @patch('app.controllers.db.connector.mariadb.connect')
    @patch('app.controllers.db.connector.load_dotenv')
    @patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "test_db"
    })
    def test_get_con_multiple_calls(self, mock_load_dotenv, mock_connect):
        """Test múltiples llamadas a get_con"""
        mock_connect.return_value = self.mock_connection
        
        # Primera llamada
        result1 = get_con()
        
        # Segunda llamada  
        result2 = get_con()
        
        # Verificar que ambas llamadas funcionan
        assert result1 == self.mock_connection
        assert result2 == self.mock_connection
        
        # Verificar que load_dotenv y connect se llamaron las veces correctas
        assert mock_load_dotenv.call_count == 2
        assert mock_connect.call_count == 2