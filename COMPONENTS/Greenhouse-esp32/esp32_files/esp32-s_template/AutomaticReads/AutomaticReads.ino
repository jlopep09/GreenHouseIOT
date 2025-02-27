#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>

/*
  NETWORK CONFIG
*/
const char* ssid = "MOVISTAR_C4BF";
const char* password = "77772EE1698861A4B165";
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
    //sensorDataHandler(); //Comprueba si es necesario realizar una nueva lectura
    //lightHandler(); //Comprueba si la configuración de luces es correcta respecto a la programada
    //TODO pumpHandler() 
    //TODO fanHandler()
    //TODO cameraHandler()
  } else {
    Serial.println("Reconectando a WiFi...");
    connectToWiFi();
  }
}

