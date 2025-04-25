#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h>
#include <NTPClient.h>
#include <WiFiUdp.h>


String horaEncendido_ox = "09:00"; // Formato HH:MM
String horaApagado_ox   = "18:00";
bool oxigenoEncendido = false;
bool modoAutomatico_ox  = true;

// --- Funciones auxiliares ---
extern String obtenerHoraActual();
extern bool horaDentroDelRango(const String& hora, String StringHoraEncendido, String StringHoraApagado);

void encenderOxigeno() {
  digitalWrite(PIN_RELE_OXIGENO, HIGH);
  oxigenoEncendido = true;
}

void apagarOxigeno() {
  digitalWrite(PIN_RELE_OXIGENO, LOW);
  oxigenoEncendido = false;
}

void aplicarEstadoOxigeno() {
  if (oxigenoEncendido) {
    encenderOxigeno();
  } else {
    apagarOxigeno();
  }
}

// --- Lógica principal de control de luces ---
void comprobarOxigeno() {
  if (modoAutomatico_ox) {
    String horaActual = obtenerHoraActual();
    bool deberianEstarEncendidas = horaDentroDelRango(horaActual, horaEncendido_ox,horaApagado_ox );

    if (deberianEstarEncendidas != oxigenoEncendido) {
      if (deberianEstarEncendidas) {
        encenderOxigeno();
      } else {
        apagarOxigeno();
      }
    }
  } else {
    aplicarEstadoOxigeno(); // En modo manual, solo aplicamos el estado actual
  }
}
// --- Setup y Loop ---
void oxigenSetup() {
  pinMode(PIN_RELE_OXIGENO, OUTPUT);
  apagarOxigeno(); // Apagar al inicio
  // Iniciar WiFi, NTP, etc.
}

