#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>


//NETWORK CONFIG
const char* ssid = "MOVISTAR_C4BF";
const char* password = "77772EE1698861A4B165";
String serverName = "http://192.168.1.44:8001/send/sensordata";
String gh_name = "Invernadero-03";

void connectToWiFi();
void sendSensorData();
bool checkLightActualStatus();
void sensorsSetup();
String generateWeb();
void endpointsSetup();
void lightHandler();
bool getLightStatus();
void sensorDataHandler();
void syncTime();

void setup() {
  Serial.begin(115200);
  connectToWiFi();
  Serial.print("ESP32 IP address: "); Serial.println(WiFi.localIP());
  sensorsSetup();
  endpointsSetup();
}




void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    syncTime();
    lightHandler();
    sensorDataHandler();
  } else {
    Serial.println("Reconectando a WiFi...");
    connectToWiFi();
  }
}

