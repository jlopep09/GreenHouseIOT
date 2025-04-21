#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>//adafruit v1.4.6
#include <ESPAsyncWebServer.h> //ESP32 Async WebServer ESP32Async v3.7.6 and Async TCP v3.3.8
#include <NTPClient.h>//Fabrice weinberg v3.2.1
#include <WiFiUdp.h>
#include <TimeLib.h>//Michael margolis v1.6.1

/*
  NETWORK CONFIG
*/
const char* ssid = "MOVISTAR_E080";
const char* password = "sjPmdBHx8Q8LkzHByiCx";
String serverName = "http://192.168.1.44:8001/send/sensordata";
String gh_name = "Invernadero-01";

// Configuración de IP estática
IPAddress local_IP(192, 168, 1, 201); // Cambia la IP según tu red local
IPAddress gateway(192, 168, 1, 1);    // Puerta de enlace (usualmente el router)
IPAddress subnet(255, 255, 255, 0);   // Máscara de subred

void connectToWiFi();
void sendSensorData();
bool checkLightActualStatus();
void sensorsSetup();
void startWeb();
void lightHandler();
bool getLightStatus();
void sensorDataHandler();
void syncTime();
void setupTime();

void setup() {
  Serial.begin(115200);
  // Establecer la IP estática antes de conectar
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("Configuración de IP estática fallida");
  }
  connectToWiFi();
  if (WiFi.status() == WL_CONNECTED) {
      Serial.print("ESP32 IP address: ");
      Serial.println(WiFi.localIP());
  } else {
      Serial.println("Reconectando a WiFi...");
  }
  Serial.println("Estableciendo configuracion horaria");
  setupTime();
  Serial.println("Inicializando los sensores");
  sensorsSetup();
  Serial.println("Iniciando servidor web");
  startWeb();
  Serial.println("Configuraciones establecidas correctamente");
}


void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    syncTime(); //Sincroniza el tiempo para los contadores utilizados en la aplicación
    sensorDataHandler(); //Comprueba si es necesario realizar una nueva lectura
    //lightHandler(); //Comprueba si la configuración de luces es correcta respecto a la programada
    //TODO pumpHandler() 
    //TODO fanHandler()
    //TODO cameraHandler()
  } else {
    Serial.println("Reconectando a WiFi...");
    connectToWiFi();
  }
}

