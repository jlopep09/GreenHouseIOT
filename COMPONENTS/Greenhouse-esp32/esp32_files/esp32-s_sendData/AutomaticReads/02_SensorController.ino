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
String lightOnTime = "09:00"; // Hora por defecto para encender. Debe tener los 4 digitos. SI -> 09:00, NO -> 9:00
String lightOffTime = "18:00"; // Hora por defecto para apagar
bool lightStatus = false; // Estado actual de las luces
bool automaticLights = true; //true -> auto, false -> manual 
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "europe.pool.ntp.org", 3600, 60000); // Sincronización con UTC

bool getLightStatus(){
  return lightStatus;
}
void syncTime(){
  timeClient.update();
}
void lightHandler(){
  if(automaticLights){
      bool needChange = checkLightActualStatus();
      if(automaticLights && needChange && automaticLights){// ees necesario volver a comprobar el modo por si justo cambia
        lightStatus = !lightStatus;
        if(lightStatus){
        //TODO encender luces digitalWrite(PINRELELUCES, HIGH);
        }else{
        //TODO apagar luces digitalWrite(PINRELELUCES, LOW);
        }
      }
    }else{
      if(lightStatus){
        //TODO encender luces digitalWrite(PINRELELUCES, HIGH);
      }else{
        //TODO apagar luces digitalWrite(PINRELELUCES, LOW);
      }
    }
}
void sensorsSetup(){
  //---------PINS AND SENSOR------------
  dht.begin();
  pinMode(WATERPOWERPIN, OUTPUT);
  digitalWrite(WATERPOWERPIN, LOW);
  //---------TIME CONFIG------------
  timeClient.begin();

  setTime(timeClient.getEpochTime()); 
}
bool checkLightActualStatus() {
  // Obtener la hora actual desde el cliente NTP
  String currentHour = timeClient.getFormattedTime().substring(0, 5); // Formato HH:MM
  
  // Comparar con las horas configuradas
  if (currentHour >= lightOnTime && currentHour < lightOffTime) {
    if(lightStatus==false){
      return true;
    }
  } else {
    if(lightStatus==true){
      return true;
    }
  }
  return false;//no necesita cambiarse
}

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