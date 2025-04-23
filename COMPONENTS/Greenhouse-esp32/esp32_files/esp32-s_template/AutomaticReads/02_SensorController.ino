#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <TimeLib.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

//INPUT PIN


//EXTRA DHT CONFIG
#define DHTTYPE DHT22    
DHT dht(DHTPIN, DHTTYPE);

void sensorsSetup(){
  //---------PINS AND SENSOR------------
  dht.begin();
}

void getSensorData(String& jsonData) {
    float temperature = dht.readTemperature();
    float humidity    = dht.readHumidity();

    int lightLevel    = analogRead(PHOTO_PIN);
    int tds            = analogRead(TDS_PIN);
    int waterTemp      = analogRead(WATER_TEMP_PIN);
    int waterLevel     = analogRead(WATER_PIN);

    String gh_ip = WiFi.localIP().toString();

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
    // 3) Sensor TDS
    if (isnan((float)tds)) {
        Serial.println("Error al leer la electro-conductividad");
        jsonData = "{\"error\":\"Failed to read TDS sensor\"}";
        return;
    }
    // 4) Sensor de temperatura de agua
    if (isnan((float)waterTemp)) {
        Serial.println("Error al leer la temperatura de agua");
        jsonData = "{\"error\":\"Failed to read water temperature sensor\"}";
        return;
    }
    // 5) Sensor de nivel de agua
    if (isnan((float)waterLevel)) {
        Serial.println("Error al leer el nivel de agua");
        jsonData = "{\"error\":\"Failed to read water level sensor\"}";
        return;
    }

    // Si todos los sensores dieron “lectura”, construimos el JSON
    jsonData  = "{";
    jsonData += "\"gh_name\":\""           + String(gh_name)            + "\",";
    jsonData += "\"gh_ip\":\""             + gh_ip                      + "\",";
    jsonData += "\"temperature\":"         + String(temperature, 2)      + ",";
    jsonData += "\"humidity\":"            + String(humidity, 2)         + ",";
    jsonData += "\"light_level\":"         + String(lightLevel)          + ",";
    jsonData += "\"tds\":"                 + String(tds)                 + ",";
    jsonData += "\"water_temperature\":"   + String(waterTemp)           + ",";
    jsonData += "\"water_level\":"         + String(waterLevel);
    jsonData += "}";
}

