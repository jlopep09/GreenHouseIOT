#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>

WiFiUDP ntpUDP;
NTPClient timeClient = NTPClient(ntpUDP, "europe.pool.ntp.org", 3600, 60000); // Sincronización con UTC

void setupTime(){
  timeClient.begin();
  setTime(timeClient.getEpochTime()); 
}

void syncTime(){
  timeClient.update();
}