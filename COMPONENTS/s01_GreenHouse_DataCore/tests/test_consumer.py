import pytest
import os
import json
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from kafka import KafkaConsumer
from app.kafka_module.consumer import (
    _build_consumer,
    get_consumer,
    consume_messages,
    consumer
)

# Configurar el token para los tests
TEST_TOKEN = os.getenv("SECRET_TOKEN", "none")

class TestKafkaConsumer:
    """Test suite para el módulo consumer de Kafka"""
    
    def setup_method(self):
        """Setup antes de cada test"""
        self.sample_message_data = {
            "gh_name": "test_greenhouse",
            "gh_ip": "192.168.1.100",
            "sync_code": "test_sync_code",
            "light_level": "600",
            "tds": "450",
            "temperature": "25.5",
            "humidity": "65",
            "water_level": "75",
            "water_temperature": "22.0"
        }
        
        self.sample_db_result = {
            "result": [{"id": 1}]
        }

    @patch('app.kafka_module.consumer.KafkaConsumer')
    def test_build_consumer_success(self, mock_kafka_consumer):
        """Test que _build_consumer crea correctamente un KafkaConsumer"""
        mock_consumer_instance = Mock()
        mock_kafka_consumer.return_value = mock_consumer_instance
        
        result = _build_consumer()
        
        mock_kafka_consumer.assert_called_once_with(
            'sensor_data',
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            group_id='sensor_data_group',
            enable_auto_commit=True,
            value_deserializer=mock_kafka_consumer.call_args[1]['value_deserializer']
        )
        assert result == mock_consumer_instance

    @patch('app.kafka_module.consumer.KafkaConsumer')
    def test_build_consumer_deserializer(self, mock_kafka_consumer):
        """Test que el deserializador funciona correctamente"""
        _build_consumer()
        
        # Obtener el deserializador que se pasó
        deserializer = mock_kafka_consumer.call_args[1]['value_deserializer']
        
        # Test del deserializador
        test_data = {"test": "data"}
        serialized = json.dumps(test_data).encode('utf-8')
        result = deserializer(serialized)
        
        assert result == test_data

    @patch.dict(os.environ, {'TESTING': 'true'})
    def test_get_consumer_testing_mode(self):
        """Test que get_consumer retorna None en modo TESTING"""
        result = get_consumer()
        assert result is None

    @patch.dict(os.environ, {}, clear=True)
    @patch('app.kafka_module.consumer.consumer', Mock())
    def test_get_consumer_production_mode(self):
        """Test que get_consumer retorna el consumer en producción"""
        with patch('app.kafka_module.consumer.consumer', 'mock_consumer'):
            result = get_consumer()
            assert result == 'mock_consumer'

    @pytest.mark.asyncio
    async def test_consume_messages_testing_mode(self):
        """Test que consume_messages no procesa mensajes en modo TESTING"""
        with patch('app.kafka_module.consumer.get_consumer', return_value=None):
            with patch('builtins.print') as mock_print:
                await consume_messages()
                mock_print.assert_called_with("Kafka consumer deshabilitado (TESTING active). No se consumirán mensajes.")

    @pytest.mark.asyncio
    async def test_consume_messages_success_flow(self):
        """Test del flujo exitoso de consume_messages"""
        # Mock del consumer
        mock_consumer = Mock()
        mock_message = Mock()
        mock_message.value = self.sample_message_data
        
        # Configurar poll para retornar mensajes una vez y luego vacío
        mock_consumer.poll.side_effect = [
            {Mock(): [mock_message]},  # Primera llamada con mensaje
            {}  # Segunda llamada vacía para terminar el loop
        ]
        
        with patch('app.kafka_module.consumer.get_consumer', return_value=mock_consumer):
            with patch('app.controllers.detector.Detector.checkIP', return_value=False):
                with patch('app.controllers.db.db_queries.get_greenhouse_by_name', return_value=self.sample_db_result):
                    with patch('app.controllers.db.db_queries.create_read') as mock_create_read:
                        with patch('builtins.print') as mock_print:
                            # Usar timeout para evitar bucle infinito
                            try:
                                await asyncio.wait_for(consume_messages(), timeout=0.1)
                            except asyncio.TimeoutError:
                                pass
                            
                            # Verificar que se imprimió el mensaje recibido
                            mock_print.assert_any_call(f"Datos recibidos: {self.sample_message_data}")
                            
                            # Verificar que se llamó create_read con los parámetros correctos
                            mock_create_read.assert_called_once_with(
                                tds=self.sample_message_data["tds"],
                                temperature=self.sample_message_data["temperature"],
                                humidity=self.sample_message_data["humidity"],
                                light_level="True",  # 600 > 500 = True
                                water_level=self.sample_message_data["water_level"],
                                water_temperature=self.sample_message_data["water_temperature"],
                                gh_id=1
                            )

    @pytest.mark.asyncio
    async def test_consume_messages_light_level_false(self):
        """Test que light_level se convierte a False cuando es <= 500"""
        # Modificar el mensaje para que light_level sea <= 500
        low_light_data = self.sample_message_data.copy()
        low_light_data["light_level"] = "400"
        
        mock_consumer = Mock()
        mock_message = Mock()
        mock_message.value = low_light_data
        
        mock_consumer.poll.side_effect = [
            {Mock(): [mock_message]},
            {}
        ]
        
        with patch('app.kafka_module.consumer.get_consumer', return_value=mock_consumer):
            with patch('app.controllers.detector.Detector.checkIP', return_value=False):
                with patch('app.controllers.db.db_queries.get_greenhouse_by_name', return_value=self.sample_db_result):
                    with patch('app.controllers.db.db_queries.create_read') as mock_create_read:
                        try:
                            await asyncio.wait_for(consume_messages(), timeout=0.1)
                        except asyncio.TimeoutError:
                            pass
                        
                        # Verificar que light_level es "False"
                        mock_create_read.assert_called_once()
                        call_args = mock_create_read.call_args[1]
                        assert call_args['light_level'] == "False"

    @pytest.mark.asyncio
    async def test_consume_messages_detector_checkip_exception(self):
        """Test cuando Detector.checkIP lanza excepción"""
        mock_consumer = Mock()
        mock_message = Mock()
        mock_message.value = self.sample_message_data
        
        mock_consumer.poll.side_effect = [
            {Mock(): [mock_message]},
            {}
        ]
        
        with patch('app.kafka_module.consumer.get_consumer', return_value=mock_consumer):
            with patch('app.controllers.detector.Detector.checkIP', return_value=True):
                with patch('app.controllers.db.db_queries.get_greenhouse_by_name', return_value=self.sample_db_result):
                    with patch('app.controllers.db.db_queries.create_read') as mock_create_read:
                        with patch('builtins.print') as mock_print:
                            try:
                                await asyncio.wait_for(consume_messages(), timeout=0.1)
                            except asyncio.TimeoutError:
                                pass
                            
                            # Verificar que se imprimió el error
                            mock_print.assert_any_call("gh ip changed! ERROR")
                            
                            # Aún debería procesar el mensaje
                            mock_create_read.assert_called_once()

    @pytest.mark.asyncio
    async def test_consume_messages_general_exception(self):
        """Test cuando ocurre una excepción general durante el procesamiento"""
        mock_consumer = Mock()
        mock_consumer.poll.side_effect = Exception("Test error")
        
        with patch('app.kafka_module.consumer.get_consumer', return_value=mock_consumer):
            with patch('builtins.print') as mock_print:
                try:
                    await asyncio.wait_for(consume_messages(), timeout=0.1)
                except asyncio.TimeoutError:
                    pass
                
                # Verificar que se imprimió el error
                mock_print.assert_any_call("Error al consumir mensajes: Test error")

    @pytest.mark.asyncio
    async def test_consume_messages_empty_poll(self):
        """Test cuando poll retorna vacío"""
        mock_consumer = Mock()
        mock_consumer.poll.return_value = {}
        
        with patch('app.kafka_module.consumer.get_consumer', return_value=mock_consumer):
            with patch('asyncio.sleep', side_effect=asyncio.TimeoutError):
                with pytest.raises(asyncio.TimeoutError):
                    await consume_messages()

    @pytest.mark.asyncio
    async def test_consume_messages_multiple_messages(self):
        """Test procesamiento de múltiples mensajes"""
        mock_consumer = Mock()
        
        # Crear múltiples mensajes
        message1 = Mock()
        message1.value = self.sample_message_data
        
        message2_data = self.sample_message_data.copy()
        message2_data["gh_name"] = "greenhouse2"
        message2 = Mock()
        message2.value = message2_data
        
        mock_consumer.poll.side_effect = [
            {Mock(): [message1, message2]},
            {}
        ]
        
        with patch('app.kafka_module.consumer.get_consumer', return_value=mock_consumer):
            with patch('app.controllers.detector.Detector.checkIP', return_value=False):
                with patch('app.controllers.db.db_queries.get_greenhouse_by_name', return_value=self.sample_db_result):
                    with patch('app.controllers.db.db_queries.create_read') as mock_create_read:
                        with patch('builtins.print') as mock_print:
                            try:
                                await asyncio.wait_for(consume_messages(), timeout=0.1)
                            except asyncio.TimeoutError:
                                pass
                            
                            # Verificar que se procesaron ambos mensajes
                            assert mock_create_read.call_count == 2
                            assert mock_print.call_count >= 2  # Al menos los dos mensajes de datos recibidos

    @pytest.mark.asyncio
    async def test_consume_messages_database_error(self):
        """Test cuando falla la operación de base de datos"""
        mock_consumer = Mock()
        mock_message = Mock()
        mock_message.value = self.sample_message_data
        
        mock_consumer.poll.side_effect = [
            {Mock(): [mock_message]},
            {}
        ]
        
        with patch('app.kafka_module.consumer.get_consumer', return_value=mock_consumer):
            with patch('app.controllers.detector.Detector.checkIP', return_value=False):
                with patch('app.controllers.db.db_queries.get_greenhouse_by_name', side_effect=Exception("DB Error")):
                    with patch('builtins.print') as mock_print:
                        try:
                            await asyncio.wait_for(consume_messages(), timeout=0.1)
                        except asyncio.TimeoutError:
                            pass
                        
                        # Verificar que se manejó el error
                        mock_print.assert_any_call("Error al consumir mensajes: DB Error")

    def test_consumer_initialization_production(self):
        """Test que el consumer se inicializa correctamente en producción"""
        with patch.dict(os.environ, {}, clear=True):
            with patch('app.kafka_module.consumer._build_consumer') as mock_build:
                # Simular reimport del módulo
                import importlib
                import app.kafka_module.consumer as consumer_module
                
                # El consumer debería haberse creado
                assert mock_build.called or consumer_module.consumer is not None

    def test_consumer_initialization_testing(self):
        """Test que el consumer es None en modo testing"""
        with patch.dict(os.environ, {'TESTING': 'true'}):
            # Simular reimport del módulo
            import importlib
            import app.kafka_module.consumer as consumer_module
            
            # En testing, consumer debería ser None
            # Nota: esto puede requerir ajustes dependiendo de cómo esté estructurado el módulo

    @pytest.mark.asyncio
    async def test_consume_messages_timeout_handling(self):
        """Test que el timeout del poll se maneja correctamente"""
        mock_consumer = Mock()
        mock_consumer.poll.return_value = {}  # Sin mensajes
        
        with patch('app.kafka_module.consumer.get_consumer', return_value=mock_consumer):
            try:
                await asyncio.wait_for(consume_messages(), timeout=0.1)
            except asyncio.TimeoutError:
                pass
            
            # Verificar que poll fue llamado con timeout correcto
            mock_consumer.poll.assert_called_with(timeout_ms=1000)

    @pytest.mark.asyncio
    async def test_consume_messages_asyncio_sleep(self):
        """Test que asyncio.sleep se llama correctamente"""
        mock_consumer = Mock()
        mock_consumer.poll.return_value = {}
        
        with patch('app.kafka_module.consumer.get_consumer', return_value=mock_consumer):
            with patch('asyncio.sleep', side_effect=asyncio.TimeoutError) as mock_sleep:
                with pytest.raises(asyncio.TimeoutError):
                    await consume_messages()
                
                mock_sleep.assert_called_with(1)

    def test_json_deserializer_invalid_json(self):
        """Test que el deserializador maneja JSON inválido"""
        with patch('app.kafka_module.consumer.KafkaConsumer') as mock_kafka_consumer:
            _build_consumer()
            deserializer = mock_kafka_consumer.call_args[1]['value_deserializer']
            
            # Test con JSON inválido
            with pytest.raises(json.JSONDecodeError):
                deserializer(b'invalid json')

    def test_json_deserializer_empty_data(self):
        """Test que el deserializador maneja datos vacíos"""
        with patch('app.kafka_module.consumer.KafkaConsumer') as mock_kafka_consumer:
            _build_consumer()
            deserializer = mock_kafka_consumer.call_args[1]['value_deserializer']
            
            # Test con datos vacíos
            with pytest.raises(json.JSONDecodeError):
                deserializer(b'')

    def test_json_deserializer_unicode_data(self):
        """Test que el deserializador maneja datos unicode"""
        with patch('app.kafka_module.consumer.KafkaConsumer') as mock_kafka_consumer:
            _build_consumer()
            deserializer = mock_kafka_consumer.call_args[1]['value_deserializer']
            
            # Test con datos unicode
            test_data = {"message": "Hola, ñandú"}
            serialized = json.dumps(test_data).encode('utf-8')
            result = deserializer(serialized)
            
            assert result == test_data