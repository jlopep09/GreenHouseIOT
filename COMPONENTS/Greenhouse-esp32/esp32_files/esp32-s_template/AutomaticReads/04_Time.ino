#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);


void setupTime(){
  timeClient.begin();
  timeClient.setTimeOffset(7200);
  if (timeClient.forceUpdate()) {
    Serial.println("Hora actualizada (force).");
  } else {
    Serial.println("No se ha podido actualizar la hora (force).");
  }
}

void syncTime(){
  if (timeClient.update()) {
    Serial.println("Hora actualizada.");
  }
}
String obtenerHoraActual() {
  return timeClient.getFormattedTime().substring(0, 5); // HH:MM
}

bool horaDentroDelRango(const String& hora, String StringHoraEncendido, String StringHoraApagado) {
  return hora >= StringHoraEncendido && hora < StringHoraApagado;
}
