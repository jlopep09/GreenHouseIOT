#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>

//WEB SERVER
AsyncWebServer server(80); 

void startWeb(){
  endpointsSetup();
}

String generateWeb() {
  String lightsMode = automaticLights ? "Auto" : "Manual";
  String light_status = lightStatus ? "ON" : "OFF";
  String gh_ip = WiFi.localIP().toString();

  return "<html>"
          "<head>"
          "<meta charset='utf-8'>"
          "<meta name='viewport' content='width=device-width, initial-scale=1'>"
          
        "</head>"
         "<body>"
         "<h1>Controles</h1>"
         "<hr>"
         "<p>IP del ESP32: <strong>" + gh_ip + "</strong></p>"
         // Formulario para cambiar el nombre del invernadero
         "<form method='POST' action='/gh_name/'>"
         "  <label>Cambiar nombre del invernadero:</label>"
         "  <input type='text' name='gh_name' placeholder='" + String(gh_name) + "'>"
         "  <button type='submit'>Actualizar</button>"
         "</form>"

         // Formulario para cambiar el serverName
         "<form method='POST' action='/serverName/'>"
         "  <label>Cambiar Server Name:</label>"
         "  <input type='text' name='serverName' placeholder='" + String(serverName) + "'>"
         "  <button type='submit'>Actualizar</button>"
         "</form>"

         // Formulario para cambiar el sendInterval
         "<form method='POST' action='/send_interval/'>"
         "  <label>Cambiar Send Interval (ms):</label>"
         "  <input type='text' name='send_interval' placeholder='" + String(sendInterval) + "'>"
         "  <button type='submit'>Actualizar</button>"
         "</form>"
         "<hr>"
         "<h2>Luces</h2>"
         "<p>Modo de luces: <strong>" + lightsMode + "</strong></p>"
         "<p>Estado actual: <strong>" + light_status + "</strong></p>"
         
         // Formulario para actualizar la hora de encendido
         "<form method='POST' action='/light/on/'>"
         "  <label>Hora de encendido:</label>"
         "  <input type='text' name='time' placeholder='" + lightOnTime + "'>"
         "  <button type='submit'>Actualizar</button>"
         "</form>"

         // Formulario para actualizar la hora de apagado
         "<form method='POST' action='/light/off/'>"
         "  <label>Hora de apagado:</label>"
         "  <input type='text' name='time' placeholder='" + lightOffTime + "'>"
         "  <button type='submit'>Actualizar</button>"
         "</form>"

         // Botón para encender las luces inmediatamente
         "<form method='POST' action='/light/on/'>"
         "  <label>Encender luces: </label>"
         "  <input type='hidden' name='now' value='true'>"
         "  <button type='submit'>ON</button>"
         "</form>"

         // Botón para apagar las luces inmediatamente
         "<form method='POST' action='/light/off/'>"
         "  <label>Apagar luces: </label>"
         "  <input type='hidden' name='now' value='true'>"
         "  <button type='submit'>OFF</button>"
         "</form>"
        "<hr>"
        "<p>GreenhouseIOT - 2024</p>"


         "</body>"
         "</html>";
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
      request->send(200, "text/plain", "Encendido de luces programado a las: " + lightOnTime);
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
      request->send(200, "text/plain", "Apagado de luces programado a las: " + lightOffTime);
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
