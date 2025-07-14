import pytest
from unittest.mock import patch, MagicMock
from app.controllers.detector import Detector

class TestDetector:
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.create_greenhouse')
    def test_checkIP_greenhouse_not_found_creates_new(self, mock_create_greenhouse, mock_get_greenhouse_by_name):
        """Test que cuando no se encuentra el greenhouse, se crea uno nuevo"""
        # Mock para simular que no se encontró el greenhouse
        mock_get_greenhouse_by_name.return_value = {"result": []}
        mock_create_greenhouse.return_value = {"id": 1, "status": "created"}
        
        # Ejecutar el método
        result = Detector.checkIP("TestGreenhouse", "192.168.1.100", "SYNC123")
        
        # Verificaciones
        assert result == False
        mock_get_greenhouse_by_name.assert_called_once_with("TestGreenhouse")
        mock_create_greenhouse.assert_called_once_with(
            name="TestGreenhouse", 
            ip="192.168.1.100", 
            sync_code="SYNC123"
        )
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.update_greenhouse_ip')
    def test_checkIP_ip_changed_updates_ip(self, mock_update_greenhouse_ip, mock_get_greenhouse_by_name):
        """Test que cuando la IP cambió, se actualiza en la base de datos"""
        # Mock para simular greenhouse encontrado con IP diferente
        mock_get_greenhouse_by_name.return_value = {
            "result": [
                {
                    "id": 1,
                    "name": "TestGreenhouse",
                    "ip": "192.168.1.50",  # IP anterior
                    "sync_code": "SYNC123"
                }
            ]
        }
        mock_update_greenhouse_ip.return_value = {"status": "updated"}
        
        # Ejecutar el método con nueva IP
        result = Detector.checkIP("TestGreenhouse", "192.168.1.100", "SYNC123")
        
        # Verificaciones
        assert result == False
        mock_get_greenhouse_by_name.assert_called_once_with("TestGreenhouse")
        mock_update_greenhouse_ip.assert_called_once_with("TestGreenhouse", "192.168.1.100")
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.update_greenhouse_ip')
    def test_checkIP_same_ip_no_update(self, mock_update_greenhouse_ip, mock_get_greenhouse_by_name):
        """Test que cuando la IP es la misma, no se actualiza"""
        # Mock para simular greenhouse encontrado con la misma IP
        mock_get_greenhouse_by_name.return_value = {
            "result": [
                {
                    "id": 1,
                    "name": "TestGreenhouse",
                    "ip": "192.168.1.100",  # Misma IP
                    "sync_code": "SYNC123"
                }
            ]
        }
        
        # Ejecutar el método con la misma IP
        result = Detector.checkIP("TestGreenhouse", "192.168.1.100", "SYNC123")
        
        # Verificaciones
        assert result == False
        mock_get_greenhouse_by_name.assert_called_once_with("TestGreenhouse")
        mock_update_greenhouse_ip.assert_not_called()  # No debe llamarse
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.create_greenhouse')
    def test_checkIP_empty_name_creates_new(self, mock_create_greenhouse, mock_get_greenhouse_by_name):
        """Test con nombre vacío (edge case)"""
        mock_get_greenhouse_by_name.return_value = {"result": []}
        mock_create_greenhouse.return_value = {"id": 1, "status": "created"}
        
        result = Detector.checkIP("", "192.168.1.100", "SYNC123")
        
        assert result == False
        mock_get_greenhouse_by_name.assert_called_once_with("")
        mock_create_greenhouse.assert_called_once_with(
            name="", 
            ip="192.168.1.100", 
            sync_code="SYNC123"
        )
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.update_greenhouse_ip')
    def test_checkIP_none_to_ip_updates(self, mock_update_greenhouse_ip, mock_get_greenhouse_by_name):
        """Test cuando la IP anterior es None y ahora hay una IP"""
        mock_get_greenhouse_by_name.return_value = {
            "result": [
                {
                    "id": 1,
                    "name": "TestGreenhouse",
                    "ip": None,  # IP anterior es None
                    "sync_code": "SYNC123"
                }
            ]
        }
        mock_update_greenhouse_ip.return_value = {"status": "updated"}
        
        result = Detector.checkIP("TestGreenhouse", "192.168.1.100", "SYNC123")
        
        assert result == False
        mock_get_greenhouse_by_name.assert_called_once_with("TestGreenhouse")
        mock_update_greenhouse_ip.assert_called_once_with("TestGreenhouse", "192.168.1.100")
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.update_greenhouse_ip')
    def test_checkIP_ip_to_none_updates(self, mock_update_greenhouse_ip, mock_get_greenhouse_by_name):
        """Test cuando la IP anterior existe y ahora es None"""
        mock_get_greenhouse_by_name.return_value = {
            "result": [
                {
                    "id": 1,
                    "name": "TestGreenhouse",
                    "ip": "192.168.1.100",  # IP anterior existe
                    "sync_code": "SYNC123"
                }
            ]
        }
        mock_update_greenhouse_ip.return_value = {"status": "updated"}
        
        result = Detector.checkIP("TestGreenhouse", None, "SYNC123")
        
        assert result == False
        mock_get_greenhouse_by_name.assert_called_once_with("TestGreenhouse")
        mock_update_greenhouse_ip.assert_called_once_with("TestGreenhouse", None)
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.update_greenhouse_ip')
    def test_checkIP_both_none_no_update(self, mock_update_greenhouse_ip, mock_get_greenhouse_by_name):
        """Test cuando ambas IPs son None"""
        mock_get_greenhouse_by_name.return_value = {
            "result": [
                {
                    "id": 1,
                    "name": "TestGreenhouse",
                    "ip": None,  # IP anterior es None
                    "sync_code": "SYNC123"
                }
            ]
        }
        
        result = Detector.checkIP("TestGreenhouse", None, "SYNC123")
        
        assert result == False
        mock_get_greenhouse_by_name.assert_called_once_with("TestGreenhouse")
        mock_update_greenhouse_ip.assert_not_called()  # No debe llamarse
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.update_greenhouse_ip')
    def test_checkIP_multiple_results_uses_first(self, mock_update_greenhouse_ip, mock_get_greenhouse_by_name):
        """Test cuando hay múltiples resultados, usa el primero"""
        mock_get_greenhouse_by_name.return_value = {
            "result": [
                {
                    "id": 1,
                    "name": "TestGreenhouse",
                    "ip": "192.168.1.50",
                    "sync_code": "SYNC123"
                },
                {
                    "id": 2,
                    "name": "TestGreenhouse",
                    "ip": "192.168.1.60",
                    "sync_code": "SYNC456"
                }
            ]
        }
        mock_update_greenhouse_ip.return_value = {"status": "updated"}
        
        result = Detector.checkIP("TestGreenhouse", "192.168.1.100", "SYNC123")
        
        assert result == False
        mock_get_greenhouse_by_name.assert_called_once_with("TestGreenhouse")
        mock_update_greenhouse_ip.assert_called_once_with("TestGreenhouse", "192.168.1.100")
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.create_greenhouse')
    def test_checkIP_special_characters_in_name(self, mock_create_greenhouse, mock_get_greenhouse_by_name):
        """Test con caracteres especiales en el nombre"""
        mock_get_greenhouse_by_name.return_value = {"result": []}
        mock_create_greenhouse.return_value = {"id": 1, "status": "created"}
        
        special_name = "Test-Greenhouse_123!@#"
        result = Detector.checkIP(special_name, "192.168.1.100", "SYNC123")
        
        assert result == False
        mock_get_greenhouse_by_name.assert_called_once_with(special_name)
        mock_create_greenhouse.assert_called_once_with(
            name=special_name,
            ip="192.168.1.100",
            sync_code="SYNC123"
        )
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.update_greenhouse_ip')
    def test_checkIP_long_ip_addresses(self, mock_update_greenhouse_ip, mock_get_greenhouse_by_name):
        """Test con direcciones IP largas o formatos especiales"""
        mock_get_greenhouse_by_name.return_value = {
            "result": [
                {
                    "id": 1,
                    "name": "TestGreenhouse",
                    "ip": "192.168.1.100:8080",
                    "sync_code": "SYNC123"
                }
            ]
        }
        mock_update_greenhouse_ip.return_value = {"status": "updated"}
        
        new_ip = "192.168.1.200:9090"
        result = Detector.checkIP("TestGreenhouse", new_ip, "SYNC123")
        
        assert result == False
        mock_get_greenhouse_by_name.assert_called_once_with("TestGreenhouse")
        mock_update_greenhouse_ip.assert_called_once_with("TestGreenhouse", new_ip)
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.create_greenhouse')
    def test_checkIP_database_exception_handling(self, mock_create_greenhouse, mock_get_greenhouse_by_name):
        """Test para manejar excepciones de base de datos"""
        mock_get_greenhouse_by_name.side_effect = Exception("Database error")
        
        # El método actual no maneja excepciones, pero el test documenta el comportamiento
        with pytest.raises(Exception):
            Detector.checkIP("TestGreenhouse", "192.168.1.100", "SYNC123")
        
        mock_get_greenhouse_by_name.assert_called_once_with("TestGreenhouse")
        mock_create_greenhouse.assert_not_called()
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.create_greenhouse')
    def test_checkIP_malformed_database_result(self, mock_create_greenhouse, mock_get_greenhouse_by_name):
        """Test con resultado malformado de la base de datos"""
        # Simular respuesta sin la clave "result"
        mock_get_greenhouse_by_name.return_value = {"error": "malformed"}
        
        # Esto debería causar un KeyError
        with pytest.raises(KeyError):
            Detector.checkIP("TestGreenhouse", "192.168.1.100", "SYNC123")
        
        mock_get_greenhouse_by_name.assert_called_once_with("TestGreenhouse")
        mock_create_greenhouse.assert_not_called()
    
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.update_greenhouse_ip')
    def test_checkIP_missing_ip_field_in_result(self, mock_update_greenhouse_ip, mock_get_greenhouse_by_name):
        """Test cuando el resultado no tiene el campo 'ip'"""
        mock_get_greenhouse_by_name.return_value = {
            "result": [
                {
                    "id": 1,
                    "name": "TestGreenhouse",
                    # Falta el campo 'ip'
                    "sync_code": "SYNC123"
                }
            ]
        }
        
        # Esto debería causar un KeyError
        with pytest.raises(KeyError):
            Detector.checkIP("TestGreenhouse", "192.168.1.100", "SYNC123")
        
        mock_get_greenhouse_by_name.assert_called_once_with("TestGreenhouse")
        mock_update_greenhouse_ip.assert_not_called()
    
    @patch('builtins.print')
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.create_greenhouse')
    def test_checkIP_print_statements_new_greenhouse(self, mock_create_greenhouse, mock_get_greenhouse_by_name, mock_print):
        """Test para verificar que se imprimen los mensajes correctos al crear nuevo greenhouse"""
        mock_get_greenhouse_by_name.return_value = {"result": []}
        mock_create_greenhouse.return_value = {"id": 1, "status": "created"}
        
        Detector.checkIP("TestGreenhouse", "192.168.1.100", "SYNC123")
        
        # Verificar que se llamaron los prints
        print_calls = mock_print.call_args_list
        assert len(print_calls) >= 2
        assert any("Invernadero creado correctamente" in str(call) for call in print_calls)
    
    @patch('builtins.print')
    @patch('app.controllers.detector.get_greenhouse_by_name')
    @patch('app.controllers.detector.update_greenhouse_ip')
    def test_checkIP_print_statements_ip_change(self, mock_update_greenhouse_ip, mock_get_greenhouse_by_name, mock_print):
        """Test para verificar que se imprimen los mensajes correctos al cambiar IP"""
        mock_get_greenhouse_by_name.return_value = {
            "result": [
                {
                    "id": 1,
                    "name": "TestGreenhouse",
                    "ip": "192.168.1.50",
                    "sync_code": "SYNC123"
                }
            ]
        }
        mock_update_greenhouse_ip.return_value = {"status": "updated"}
        
        Detector.checkIP("TestGreenhouse", "192.168.1.100", "SYNC123")
        
        # Verificar que se llamaron los prints
        print_calls = mock_print.call_args_list
        assert len(print_calls) >= 2
        assert any("Se ha detectado un cambio de ip" in str(call) for call in print_calls)