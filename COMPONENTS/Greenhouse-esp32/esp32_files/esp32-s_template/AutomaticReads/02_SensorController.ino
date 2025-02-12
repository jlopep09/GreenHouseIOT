#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>

//INPUT PIN
#define PHOTO_PIN 32
#define WATER_PIN 34
#define MOIST_PIN 35
#define DHTPIN 19 

//OUTPUT PIN
#define WATERPOWERPIN 33

//EXTRA DHT CONFIG
#define DHTTYPE DHT22    
DHT dht(DHTPIN, DHTTYPE);

//TIME CONFIG
unsigned long previousMillis = 0; // Almacena el tiempo del último envío
unsigned long sendInterval = 30000; // Intervalo de envío en milisegundos (30 segundos)




void sensorsSetup(){
  //---------PINS AND SENSOR------------
  dht.begin();
  pinMode(WATERPOWERPIN, OUTPUT);
  digitalWrite(WATERPOWERPIN, LOW);

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
    int moist = analogRead(MOIST_PIN);
    String gh_ip = WiFi.localIP().toString();

    digitalWrite(WATERPOWERPIN, HIGH);
    int waterlevel = analogRead(WATER_PIN);
    digitalWrite(WATERPOWERPIN, LOW);

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Error al leer el sensor DHT22");
      return;
    }

    // Crear el JSON
    String postData = "{\"gh_name\": \"" + String(gh_name) + 
                      "\", \"gh_ip\": \"" + gh_ip + 
                      "\", \"temperature\": " + String(temperature) + 
                      ", \"humidity\": " + String(humidity) + 
                      ", \"water_level\": " + String(waterlevel) + 
                      ", \"moist\": " + String(moist) +
                      ", \"light_level\": " + String(lightLevel) + "}";

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