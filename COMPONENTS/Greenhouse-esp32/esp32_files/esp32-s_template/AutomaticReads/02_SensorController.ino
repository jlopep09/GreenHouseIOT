#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <TimeLib.h>
#include <NTPClient.h>
#include <WiFiUdp.h>



//INPUT PIN

#define TDS_PIN 4
#define WATER_PIN 5
#define WATER_TEMP_PIN 6
#define DHTPIN 7
#define PHOTO_PIN 15

//EXTRA DHT CONFIG
#define DHTTYPE DHT22    
DHT dht(DHTPIN, DHTTYPE);

extern NTPClient timeClient;

//TIME CONFIG
unsigned long previousMillis = 0; // Almacena el tiempo del último envío
unsigned long sendInterval = 30000; // Intervalo de envío en milisegundos (30 segundos)




void sensorsSetup(){
  //---------PINS AND SENSOR------------
  dht.begin();

}

/*
  Esta función es la encargada de comprobar si ha pasado el tiempo necesario para realizar una nueva
  lectura de datos. Se ha utilizado un contador en lugar de un sleep para evitar que se congele el 
  servidor web y otros procesos relacionados al invernadero.

*/
void sensorDataHandler(){
      // Lógica de envío de datos
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= sendInterval) {
      previousMillis = currentMillis;
      Serial.print("Hora actual: ");
      Serial.println(timeClient.getFormattedTime());
      Serial.print("Luces: ");
      Serial.println(getLightStatus());
      sendSensorData();
    }
}
void sendSensorData(){
    HTTPClient http;

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    int lightLevel = analogRead(PHOTO_PIN);

    int tds = analogRead(TDS_PIN);

    int water_temp = analogRead(WATER_TEMP_PIN);

    int waterlevel = analogRead(WATER_PIN);

    String gh_ip = WiFi.localIP().toString();

   
    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Error al leer el sensor DHT22");
      return;
    }
    if (isnan(lightLevel)) {
      Serial.println("Error al leer el sensor de luz");
      return;
    }
    if (isnan(tds)) {
      Serial.println("Error al leer la electro-conductividad");
      return;
    }
    if (isnan(water_temp)) {
      Serial.println("Error al leer la temperatura de agua");
      return;
    }
    if (isnan(waterlevel)) {
      Serial.println("Error al leer el nivel de agua");
      return;
    }

    // Crear el JSON
    String postData = "{\"gh_name\": \"" + String(gh_name) + 
                      "\", \"gh_ip\": \"" + gh_ip + 
                      "\", \"temperature\": " + String(temperature) + 
                      ", \"humidity\": " + String(humidity) + 
                      ", \"water_level\": " + String(waterlevel) + 
                      ", \"tds\": " + String(tds) +
                      ", \"water_temperature\": " + String(water_temp) +
                      ", \"light_level\": " + String(lightLevel) + "}";
    Serial.println("Enviando la siguiente informacion:");
    Serial.println(postData);
    // Inicia la conexión al endpoint FastAPI
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Envía el POST y recibe la respuesta
    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Respuesta del servidor: " + response);
    } else {
      Serial.println("Error en la solicitud: " + String(httpResponseCode));
    }
    http.end();
}
void getSensorData(String& jsonData) {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int lightLevel = analogRead(PHOTO_PIN);
    int waterLevel = analogRead(WATER_PIN);
    int tds = 0; // Cambiar si se activa la lectura de TDS
    int water_temp = 0;
    String gh_ip = WiFi.localIP().toString();
    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Error al leer el sensor DHT22");
        jsonData = "{\"error\": \"Failed to read DHT22 sensor\"}";
        return;
    }

    // Crear el JSON con los datos
    jsonData = "{\"gh_name\": \"" + String(gh_name) + 
              "\", \"gh_ip\": \"" + gh_ip + 
              "\", \"temperature\": " + String(temperature) + 
              ", \"humidity\": " + String(humidity) + 
              ", \"water_level\": " + String(waterLevel) + 
              ", \"tds\": " + String(tds) +
              ", \"water_temperature\": " + String(water_temp) +
              ", \"light_level\": " + String(lightLevel) + "}";
}