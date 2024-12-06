#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>

//WEB SERVER
AsyncWebServer server(80); 



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