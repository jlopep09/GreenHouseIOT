#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>

extern bool   lucesEncendidas;     // LUCES
extern bool   modoAutomatico;      // LUCES
extern String horaEncendido;       // LUCES
extern String horaApagado;         // LUCES

extern bool   oxigenoEncendido;    // OXIGENO
extern bool   modoAutomatico_ox;   // OXIGENO
extern String horaEncendido_ox;    // OXIGENO
extern String horaApagado_ox;      // OXIGENO

extern bool ventiladorEncendido;   //VENTILADOR
extern bool modoAutomatico_fan;    //VENTILADOR
extern String horaEncendido_fan;   //VENTILADOR
extern String horaApagado_fan;     //VENTILADOR

extern bool bombaEncendido;        //BOMBA
extern String obtenerHoraActual();

//WEB SERVER
AsyncWebServer server(80); 
void getSensorData(String& jsonData);

void startWeb(){
  endpointsSetup();
}

String generateWeb() {
  String lightsMode = modoAutomatico   ? "Auto" : "Manual";
  String light_status = lucesEncendidas ? "ON"  : "OFF";
  String oxigenMode = modoAutomatico_ox  ? "Auto" : "Manual";
  String oxigen_status = oxigenoEncendido ? "ON"  : "OFF";
  String fanMode = modoAutomatico_fan  ? "Auto" : "Manual";
  String fan_status = ventiladorEncendido ? "ON"  : "OFF";
  String pump_status = bombaEncendido ? "ON"  : "OFF";
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
         "<p>Hora actual: <strong>" + obtenerHoraActual() + "</strong></p>"
         // Formulario para cambiar el nombre del invernadero
         "<form method='POST' action='/gh_name/'>"
         "  <label>Cambiar nombre del invernadero:</label>"
         "  <input type='text' name='gh_name' placeholder='" + String(gh_name) + "'>"
         "  <button type='submit'>Actualizar</button>"
         "</form>"

         "<hr>"
         "<h2>Luces</h2>"
         "<p>Modo de luces: <strong>" + lightsMode + "</strong></p>"
         "<p>Estado actual: <strong>" + light_status + "</strong></p>"
         
         // Formulario para actualizar la hora de encendido
         "<form method='POST' action='/light/on/'>"
         "  <label>Hora de encendido:</label>"
         "  <input type='text' name='time' placeholder='" + horaEncendido + "'>"
         "  <button type='submit'>Actualizar</button>"
         "</form>"

         // Formulario para actualizar la hora de apagado
         "<form method='POST' action='/light/off/'>"
         "  <label>Hora de apagado:</label>"
         "  <input type='text' name='time' placeholder='" + horaApagado  + "'>"
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
         "<h2>Oxígeno</h2>"
         "<p>Modo de oxígeno: <strong>" + oxigenMode + "</strong></p>"
         "<p>Estado actual: <strong>" + oxigen_status + "</strong></p>"
         
         // Formulario para actualizar la hora de encendido
         "<form method='POST' action='/oxigen/on/'>"
         "  <label>Hora de encendido:</label>"
         "  <input type='text' name='time' placeholder='" + horaEncendido_ox + "'>"
         "  <button type='submit'>Actualizar</button>"
         "</form>"

         // Formulario para actualizar la hora de apagado
         "<form method='POST' action='/oxigen/off/'>"
         "  <label>Hora de apagado:</label>"
         "  <input type='text' name='time' placeholder='" + horaApagado_ox  + "'>"
         "  <button type='submit'>Actualizar</button>"
         "</form>"

         // Botón para encender las luces inmediatamente
         "<form method='POST' action='/oxigen/on/'>"
         "  <label>Encender oxígeno: </label>"
         "  <input type='hidden' name='now' value='true'>"
         "  <button type='submit'>ON</button>"
         "</form>"

         // Botón para apagar las luces inmediatamente
         "<form method='POST' action='/oxigen/off/'>"
         "  <label>Apagar oxígeno: </label>"
         "  <input type='hidden' name='now' value='true'>"
         "  <button type='submit'>OFF</button>"
         "</form>"

        "<hr>"
         "<h2>Ventilador</h2>"
         "<p>Modo de ventilador: <strong>" + fanMode + "</strong></p>"
         "<p>Estado actual: <strong>" + fan_status + "</strong></p>"
         
         // Formulario para actualizar la hora de encendido
         "<form method='POST' action='/fan/on/'>"
         "  <label>Hora de encendido:</label>"
         "  <input type='text' name='time' placeholder='" + horaEncendido_fan + "'>"
         "  <button type='submit'>Actualizar</button>"
         "</form>"

         // Formulario para actualizar la hora de apagado
         "<form method='POST' action='/fan/off/'>"
         "  <label>Hora de apagado:</label>"
         "  <input type='text' name='time' placeholder='" + horaApagado_fan  + "'>"
         "  <button type='submit'>Actualizar</button>"
         "</form>"

         // Botón para encender las luces inmediatamente
         "<form method='POST' action='/fan/on/'>"
         "  <label>Encender ventilador: </label>"
         "  <input type='hidden' name='now' value='true'>"
         "  <button type='submit'>ON</button>"
         "</form>"

         // Botón para apagar las luces inmediatamente
         "<form method='POST' action='/fan/off/'>"
         "  <label>Apagar ventilador: </label>"
         "  <input type='hidden' name='now' value='true'>"
         "  <button type='submit'>OFF</button>"
         "</form>"

        "<hr>"

         "<h2>Bomba</h2>"

         "<p>Estado actual: <strong>" + pump_status + "</strong></p>"

         // Botón para encender las luces inmediatamente
         "<form method='POST' action='/pump/on/'>"
         "  <label>Encender bomba: </label>"
         "  <input type='hidden' name='now' value='true'>"
         "  <button type='submit'>ON</button>"
         "</form>"

         // Botón para apagar las luces inmediatamente
         "<form method='POST' action='/pump/off/'>"
         "  <label>Apagar bomba: </label>"
         "  <input type='hidden' name='now' value='true'>"
         "  <button type='submit'>OFF</button>"
         "</form>"

        "<hr>"
        "<p>GreenhouseIOT - 2025</p>"


         "</body>"
         "</html>";
}
void endpointsSetup(){
  Serial.println("Iniciando endpoints");
  server.on("/", HTTP_GET, [](AsyncWebServerRequest* request) { 
	  Serial.println("ESP32 Web Server: New request received:");  // for debugging 
	  Serial.println("GET /");        // for debugging 
	  request->send(200, "text/html", generateWeb());}); 
     // Define a POST route to receive the light time

  server.on("/read", HTTP_GET, [](AsyncWebServerRequest* request) { 
      Serial.println("ESP32 Web Server: GET /read request received");  

      String jsonResponse;
      getSensorData(jsonResponse); // Llama a la función y obtiene los datos en JSON

      // Si el JSON comienza con {"error":, devolvemos 500
      if (jsonResponse.startsWith("{\"error\":")) {
          request->send(500, "application/json", jsonResponse);
      } else {
          request->send(200, "application/json", jsonResponse);
      }
  });

  server.on("/light/on/", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("time", true)) {
      horaEncendido = request->getParam("time", true)->value();
      modoAutomatico  = true;
      request->send(200, "text/plain", "Encendido programado a las: " + horaEncendido);
    }
    else if (request->hasParam("now", true)) {
      modoAutomatico   = false;
      lucesEncendidas = true;
      request->send(200, "text/plain", "Luces ENCENDIDAS ahora");
    }
    else {
      request->send(400, "text/plain", "Usa 'time' o 'now', no ambos.");
    }
  });
  server.on("/light/off/", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("time", true)) {
      horaApagado    = request->getParam("time", true)->value();
      modoAutomatico = true;
      request->send(200, "text/plain", "Apagado programado a las: " + horaApagado);
    }
    else if (request->hasParam("now", true)) {
      modoAutomatico   = false;
      lucesEncendidas = false;
      request->send(200, "text/plain", "Luces APAGADAS ahora");
    }
    else {
      request->send(400, "text/plain", "Usa 'time' o 'now', no ambos.");
    }
  });
    server.on("/oxigen/on/", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("time", true)) {
      horaEncendido_ox = request->getParam("time", true)->value();
      modoAutomatico_ox  = true;
      request->send(200, "text/plain", "Encendido de oxigeno programado a las: " + horaEncendido_ox);
    }
    else if (request->hasParam("now", true)) {
      modoAutomatico_ox   = false;
      oxigenoEncendido = true;
      request->send(200, "text/plain", "Oxigeno ENCENDIDO ahora");
    }
    else {
      request->send(400, "text/plain", "Usa 'time' o 'now', no ambos.");
    }
  });
  server.on("/oxigen/off/", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("time", true)) {
      horaApagado_ox    = request->getParam("time", true)->value();
      modoAutomatico_ox = true;
      request->send(200, "text/plain", "Apagado de oxigeno programado a las: " + horaApagado_ox);
    }
    else if (request->hasParam("now", true)) {
      modoAutomatico_ox   = false;
      oxigenoEncendido = false;
      request->send(200, "text/plain", "Oxigeno APAGADO ahora");
    }
    else {
      request->send(400, "text/plain", "Usa 'time' o 'now', no ambos.");
    }
  });
      server.on("/fan/on/", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("time", true)) {
      horaEncendido_fan = request->getParam("time", true)->value();
      modoAutomatico_fan  = true;
      request->send(200, "text/plain", "Encendido de ventilador programado a las: " + horaEncendido_fan);
    }
    else if (request->hasParam("now", true)) {
      modoAutomatico_fan   = false;
      ventiladorEncendido = true;
      request->send(200, "text/plain", "Ventilador ENCENDIDO ahora");
    }
    else {
      request->send(400, "text/plain", "Usa 'time' o 'now', no ambos.");
    }
  });
  server.on("/fan/off/", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("time", true)) {
      horaApagado_fan    = request->getParam("time", true)->value();
      modoAutomatico_fan = true;
      request->send(200, "text/plain", "Apagado de ventilador programado a las: " + horaApagado_fan);
    }
    else if (request->hasParam("now", true)) {
      modoAutomatico_fan   = false;
      ventiladorEncendido = false;
      request->send(200, "text/plain", "Ventilador APAGADO ahora");
    }
    else {
      request->send(400, "text/plain", "Usa 'time' o 'now', no ambos.");
    }
  });
        server.on("/pump/on/", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("now", true)) {

      bombaEncendido = true;
      request->send(200, "text/plain", "Bomba ENCENDIDA ahora");
    }
    else {
      request->send(400, "text/plain", "Usa 'now'");
    }
  });
  server.on("/pump/off/", HTTP_POST, [](AsyncWebServerRequest* request) {
    if (request->hasParam("now", true)) {

      bombaEncendido = false;
      request->send(200, "text/plain", "Bomba APAGADA ahora");
    }
    else {
      request->send(400, "text/plain", "Usa 'now'");
    }
  });
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


	 // Start the server
   Serial.println("Iniciando servidor");
	 server.begin(); 
}
