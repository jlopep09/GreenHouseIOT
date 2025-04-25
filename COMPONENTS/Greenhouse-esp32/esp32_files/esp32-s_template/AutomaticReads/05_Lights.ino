#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h>
#include <NTPClient.h>
#include <WiFiUdp.h>


String horaEncendido = "09:00"; // Formato HH:MM
String horaApagado   = "18:00";
bool lucesEncendidas = false;
bool modoAutomatico  = true;

// --- Funciones auxiliares ---
extern String obtenerHoraActual();
extern bool horaDentroDelRango(const String& hora, String StringHoraEncendido, String StringHoraApagado);


void encenderLuces() {
  digitalWrite(PIN_RELE_LUCES, HIGH);
  lucesEncendidas = true;
}

void apagarLuces() {
  digitalWrite(PIN_RELE_LUCES, LOW);
  lucesEncendidas = false;
}

void aplicarEstadoLuces() {
  if (lucesEncendidas) {
    encenderLuces();
  } else {
    apagarLuces();
  }
}

// --- Lógica principal de control de luces ---
void comprobarLuces() {
  if (modoAutomatico) {
    String horaActual = obtenerHoraActual();
    bool deberianEstarEncendidas = horaDentroDelRango(horaActual, horaEncendido,horaApagado);

    if (deberianEstarEncendidas != lucesEncendidas) {
      if (deberianEstarEncendidas) {
        encenderLuces();
      } else {
        apagarLuces();
      }
    }
  } else {
    aplicarEstadoLuces(); // En modo manual, solo aplicamos el estado actual
  }
}
// --- Setup y Loop ---
void lightSetup() {
  pinMode(PIN_RELE_LUCES, OUTPUT);
  apagarLuces(); // Apagar al inicio
  // Iniciar WiFi, NTP, etc.
}

