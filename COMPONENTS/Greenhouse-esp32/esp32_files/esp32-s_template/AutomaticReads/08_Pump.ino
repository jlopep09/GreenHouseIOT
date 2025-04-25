#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h>
#include <NTPClient.h>
#include <WiFiUdp.h>


bool bombaEncendido = false;

void encenderBomba() {
  digitalWrite(PIN_RELE_PUMP, HIGH);
  bombaEncendido = true;
}

void apagarBomba() {
  digitalWrite(PIN_RELE_PUMP, LOW);
  bombaEncendido = false;
}

// --- Lógica principal de control de luces ---
void comprobarBomba() {
  if (bombaEncendido) {
    encenderBomba();
  } else {
    apagarBomba();
  }
}
// --- Setup y Loop ---
void pumpSetup() {
  pinMode(PIN_RELE_PUMP, OUTPUT);
  apagarBomba(); // Apagar al inicio
  // Iniciar WiFi, NTP, etc.
}

