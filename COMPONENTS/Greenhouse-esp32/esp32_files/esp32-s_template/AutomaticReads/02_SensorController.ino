#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <OneWire.h>// by Jim Studt
#include <DallasTemperature.h> //by Miles Burton
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <EEPROM.h>

//EXTRA DHT CONFIG
#define DHTTYPE DHT22  

DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(WATER_TEMP_PIN);
DallasTemperature sensors(&oneWire);

float tdsValue = 0;

// Función para leer TDS sin calibración
float readTDS(float temperature) {
    int rawADC = analogRead(TDS_PIN);
    float voltage = rawADC * (3.3 / 4096.0);
    
    // Compensación de temperatura (coeficiente estándar: 0.02 por °C)
    float compensationCoefficient = 1.0 + 0.02 * (temperature - 25.0);
    float compensatedVoltage = voltage / compensationCoefficient;
    
    // SENSOR FUNCIONA AL REVÉS: Mayor conductividad = Menor voltaje
    // Voltaje en aire (sin conductividad): ~3.0V
    // Voltaje en agua: ~2.85V para 300 TDS
    
    float tdsValue = 0;
    
    if (compensatedVoltage < 3.0) {
        // Calcular TDS basado en la diferencia desde el voltaje máximo
        float voltageDrop = 3.0 - compensatedVoltage;
        
        // Factor de conversión: 0.15V drop = 300 TDS
        // Por lo tanto: TDS = voltageDrop * (300/0.15) = voltageDrop * 2000
        tdsValue = voltageDrop * 2000;
        
        // Limitar a rango realista (0-2000 ppm)
        if (tdsValue > 2000) {
            tdsValue = 2000;
        }
    } else {
        // Voltaje >= 3.0V = sin conductividad (aire)
        tdsValue = 0;
    }
    
    return tdsValue > 0 ? tdsValue : 0;
}

void sensorsSetup(){
  //---------PINS AND SENSOR------------
  dht.begin();
  sensors.begin();
  Serial.println("DS18B20 iniciado");
  
  // Configurar pin TDS como entrada analógica
  pinMode(TDS_PIN, INPUT);
  
  // Agregar debug para verificar configuración
  Serial.println("TDS sensor configurado:");
  Serial.println("Pin: " + String(TDS_PIN));
  Serial.println("Vref: 3.3V");
  Serial.println("ADC Range: 4096");
}

void getSensorData(String& jsonData) {
    float temperature = dht.readTemperature();
    float humidity    = dht.readHumidity();
    int lightLevel    = analogRead(PHOTO_PIN);

    sensors.requestTemperatures();
    float waterTemp     = sensors.getTempCByIndex(0);

    int waterLevel     = analogRead(WATER_PIN);

    String gh_ip = WiFi.localIP().toString();
    String sync_code = "GH12SHh9427Hla";

    // 1) Sensor DHT22
    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Error al leer el sensor DHT22");
        jsonData = "{\"error\":\"Failed to read DHT22 sensor\"}";
        return;
    }
    // 2) Sensor de luz
    if (isnan((float)lightLevel)) {
        Serial.println("Error al leer el sensor de luz");
        jsonData = "{\"error\":\"Failed to read light sensor\"}";
        return;
    }

    // 4) Sensor de temperatura de agua
    if (isnan((float)waterTemp)) {
        Serial.println("Error al leer la temperatura de agua");
        jsonData = "{\"error\":\"Failed to read water temperature sensor\"}";
        return;
    }
    if (waterTemp == DEVICE_DISCONNECTED_C) {
        Serial.println("Error al leer la temperatura de agua");
        jsonData = "{\"error\":\"Failed to read water temperature sensor\"}";
        return;
    }
    
    // Debug: mostrar valores del ADC antes de procesar TDS
    int rawADC = analogRead(TDS_PIN);
    float voltage = rawADC * (3.3 / 4096.0);
    Serial.println("Raw ADC value: " + String(rawADC));
    Serial.println("Voltage: " + String(voltage, 3) + "V");
    Serial.println("Water temperature: " + String(waterTemp));
    
    // Calcular la caída de voltaje desde el máximo
    float voltageDrop = 3.0 - voltage;
    Serial.println("Voltage drop from max: " + String(voltageDrop, 3) + "V");
    
    // Calcular TDS usando función directa
    float tds = readTDS(waterTemp);
    
    // Debug: mostrar valor TDS calculado
    Serial.println("TDS calculated: " + String(tds));
    
    // 3) Sensor TDS - Cambiar validación para permitir 0.0 válido
    if (isnan(tds)) {
        Serial.println("Error al leer la electro-conductividad");
        jsonData = "{\"error\":\"Failed to read TDS sensor\"}";
        return;
    }
    
    // 5) Sensor de nivel de agua
    if (isnan((float)waterLevel)) {
        Serial.println("Error al leer el nivel de agua");
        jsonData = "{\"error\":\"Failed to read water level sensor\"}";
        return;
    }

    // Si todos los sensores dieron "lectura", construimos el JSON
    jsonData  = "{";
    jsonData += "\"gh_name\":\""           + String(gh_name)            + "\",";
    jsonData += "\"sync_code\":\""           + sync_code           + "\",";
    jsonData += "\"gh_ip\":\""             + gh_ip                      + "\",";
    jsonData += "\"temperature\":"         + String(temperature, 2)      + ",";
    jsonData += "\"humidity\":"            + String(humidity, 2)         + ",";
    jsonData += "\"light_level\":"         + String(lightLevel)          + ",";
    jsonData += "\"tds\":"                 + String(tds, 2)              + ",";  // Agregar precisión decimal
    jsonData += "\"water_temperature\":"   + String(waterTemp)           + ",";
    jsonData += "\"water_level\":"         + String(waterLevel);
    jsonData += "}";
}