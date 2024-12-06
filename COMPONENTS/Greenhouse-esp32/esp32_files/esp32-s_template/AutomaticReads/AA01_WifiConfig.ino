#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>



void connectToWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a WiFi!");
}

void endpointsSetup(){
  server.on("/", HTTP_GET, [](AsyncWebServerRequest* request) { 
	  Serial.println("ESP32 Web Server: New request received:");  // for debugging 
	  Serial.println("GET /");        // for debugging 
	  request->send(200, "text/html", generateWeb());}); 
     // Define a POST route to receive the light time
  server.on("/light/on/", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("time", true)) {
      lightOnTime = request->getParam("time", true)->value();
      Serial.println("Las luces se encenderán a las: " + lightOnTime);
      automaticLights = true;
      request->send(200, "text/plain", "Las luces se encenderán a las: " + lightOnTime);
    }else if(request->hasParam("now", true)){
      Serial.println("Encendiendo luces...");
      automaticLights = false;
      lightStatus = true;
      request->send(200, "text/plain", "Encendiendo luces...");
    }else {
      request->send(400, "text/plain", "Debes usar el parámetro 'time' o el parámetro 'now'. No uses ambos a la vez.");
    }});
  server.on("/light/off/", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("time", true)) {
      lightOffTime = request->getParam("time", true)->value();
      Serial.println("Las luces se apagarán a las: " + lightOffTime);
      automaticLights = true;
      request->send(200, "text/plain", "Las luces se apagarán a las: " + lightOffTime);
    }else if(request->hasParam("now", true)){
      Serial.println("Apagando luces...");
      automaticLights = false;
      lightStatus = false;
      request->send(200, "text/plain", "Apagando luces...");
    }else {
      request->send(400, "text/plain", "Debes usar el parámetro 'time' o el parámetro 'now'. No uses ambos a la vez.");
    }});

    // Ruta para actualizar gh_name
  server.on("/gh_name", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("gh_name", true)) {
      gh_name = request->getParam("gh_name", true)->value().c_str();
      Serial.println("Nombre del invernadero actualizado a: " + String(gh_name));
      request->send(200, "text/plain", "Nombre del invernadero actualizado a: " + String(gh_name));
    } else {
      request->send(400, "text/plain", "Parámetro 'gh_name' faltante.");
    }
  });

  // Ruta para actualizar serverName
  server.on("/server_name", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("server_name", true)) {
      serverName = request->getParam("server_name", true)->value().c_str();
      Serial.println("ServerName actualizado a: " + String(serverName));
      request->send(200, "text/plain", "ServerName actualizado a: " + String(serverName));
    } else {
      request->send(400, "text/plain", "Parámetro 'server_name' faltante.");
    }
  });

  // Ruta para actualizar sendInterval
  server.on("/send_interval", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("send_interval", true)) {
      String intervalStr = request->getParam("send_interval", true)->value();
      sendInterval = intervalStr.toInt();
      Serial.println("Intervalo de envío actualizado a: " + String(sendInterval) + " ms");
      request->send(200, "text/plain", "Intervalo de envío actualizado a: " + String(sendInterval) + " ms");
    } else {
      request->send(400, "text/plain", "Parámetro 'send_interval' faltante.");
    }
  });

	 // Start the server 
	 server.begin(); 
}
