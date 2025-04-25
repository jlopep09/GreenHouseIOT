#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <NTPClient.h>
#include <WiFiUdp.h>


WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "europe.pool.ntp.org", 7200, 60000);


void setupTime(){
  timeClient.begin();
}

void syncTime(){
  timeClient.update();
}
String obtenerHoraActual() {
  return timeClient.getFormattedTime().substring(0, 5); // HH:MM
}

bool horaDentroDelRango(const String& hora, String StringHoraEncendido, String StringHoraApagado) {
  return hora >= StringHoraEncendido && hora < StringHoraApagado;
}
