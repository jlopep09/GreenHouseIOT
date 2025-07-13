#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>//DHT sensor library adafruit v1.4.6
#include <ESPAsyncWebServer.h> //ESP32 Async WebServer ESP32Async v3.7.6 and Async TCP v3.3.8 ->v3.7.7 && v3.4.0
#include <NTPClient.h>//NTPClient-Fabrice weinberg v3.2.1
#include <WiFiUdp.h>
#include <OneWire.h>// by Jim Studt
#include <DallasTemperature.h> //by Miles Burton
//Michael margolis v1.6.1
//Adafruit unified sensor v 1.1.15

//PIN SETUP

int TDS_PIN = 4;
int WATER_PIN = 5;
int WATER_TEMP_PIN = 15;
int DHTPIN = 6;
int PHOTO_PIN = 7;

int PIN_RELE_LUCES = 42;
int PIN_RELE_OXIGENO = 39;
int PIN_RELE_FAN = 41;
int PIN_RELE_PUMP = 40;

/*
  NETWORK CONFIG
*/
const char* ssid = "MOVISTAR_E080";
const char* password = "sjPmdBHx8Q8LkzHByiCx";
String gh_name = "Invernadero-01";

// Configuración de IP estática
IPAddress local_IP(192, 168, 1, 201); // Cambia la IP según tu red local
IPAddress gateway(192, 168, 1, 1);    // Puerta de enlace (usualmente el router)
IPAddress subnet(255, 255, 255, 0);   // Máscara de subred
IPAddress primaryDNS(8,8,8,8);    // Google DNS
IPAddress secondaryDNS(8,8,4,4);  // Google DNS

void connectToWiFi();
void sensorsSetup();
void lightSetup();
void startWeb();
void comprobarLuces();
void oxigenSetup();
void comprobarOxigeno();

void syncTime();
void setupTime();

void fanSetup();
void comprobarVentilador();
void pumpSetup();
void comprobarBomba();



void setup() {
  Serial.begin(115200);
  // Establecer la IP estática antes de conectar
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
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
  Serial.println("Inicializando los sensores y otros dispositivos");
  sensorsSetup();
  lightSetup();
  oxigenSetup();
  fanSetup();
  pumpSetup();
  Serial.println("Iniciando servidor web");
  startWeb();
  Serial.println("Configuraciones establecidas correctamente");
}


void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    syncTime(); //Sincroniza el tiempo para los contadores utilizados en la aplicación
    comprobarLuces(); //Comprueba si la configuración de luces es correcta respecto a la programada
    comprobarOxigeno();
    comprobarVentilador();
    comprobarBomba();
  } else {
    Serial.println("Reconectando a WiFi...");
    connectToWiFi();
  }
}

