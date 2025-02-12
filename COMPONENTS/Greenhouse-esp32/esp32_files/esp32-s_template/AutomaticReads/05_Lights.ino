#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h> 
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>

String lightOnTime = "09:00"; // Hora por defecto para encender. Debe tener los 4 digitos. SI -> 09:00, NO -> 9:00
String lightOffTime = "18:00"; // Hora por defecto para apagar
bool lightStatus = false; // Estado actual de las luces
bool automaticLights = true; //true -> auto, false -> manual 

bool getLightStatus(){
  return lightStatus;
}

void lightHandler(){
  if(automaticLights){
      bool needChange = checkLightActualStatus();
      if(automaticLights && needChange && automaticLights){// ees necesario volver a comprobar el modo por si justo cambia
        lightStatus = !lightStatus;
        if(lightStatus){
        //TODO encender luces digitalWrite(PINRELELUCES, HIGH);
        }else{
        //TODO apagar luces digitalWrite(PINRELELUCES, LOW);
        }
      }
    }else{
      if(lightStatus){
        //TODO encender luces digitalWrite(PINRELELUCES, HIGH);
      }else{
        //TODO apagar luces digitalWrite(PINRELELUCES, LOW);
      }
    }
}
bool checkLightActualStatus() {
  // Obtener la hora actual desde el cliente NTP
  String currentHour = timeClient.getFormattedTime().substring(0, 5); // Formato HH:MM
  
  // Comparar con las horas configuradas
  if (currentHour >= lightOnTime && currentHour < lightOffTime) {
    if(lightStatus==false){
      return true;
    }
  } else {
    if(lightStatus==true){
      return true;
    }
  }
  return false;//no necesita cambiarse
}