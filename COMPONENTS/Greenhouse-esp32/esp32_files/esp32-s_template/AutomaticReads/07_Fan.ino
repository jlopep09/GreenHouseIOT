#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ESPAsyncWebServer.h>
#include <NTPClient.h>
#include <WiFiUdp.h>


String horaEncendido_fan = "09:00"; // Formato HH:MM
String horaApagado_fan   = "18:00";
bool ventiladorEncendido = false;
bool modoAutomatico_fan  = true;

// --- Funciones auxiliares ---
extern String obtenerHoraActual();
extern bool horaDentroDelRango(const String& hora, String StringHoraEncendido, String StringHoraApagado);

void encenderVentilador() {
  digitalWrite(PIN_RELE_FAN, HIGH);
  ventiladorEncendido = true;
}

void apagarVentilador() {
  digitalWrite(PIN_RELE_FAN, LOW);
  ventiladorEncendido = false;
}

void aplicarEstadoVentilador() {
  if (ventiladorEncendido) {
    encenderVentilador();
  } else {
    apagarVentilador();
  }
}

// --- Lógica principal de control de luces ---
void comprobarVentilador() {
  if (modoAutomatico_fan) {
    String horaActual = obtenerHoraActual();
    bool deberianEstarEncendidas = horaDentroDelRango(horaActual, horaEncendido_fan,horaApagado_fan );

    if (deberianEstarEncendidas != ventiladorEncendido) {
      if (deberianEstarEncendidas) {
        encenderVentilador();
      } else {
        apagarVentilador();
      }
    }
  } else {
    aplicarEstadoVentilador(); // En modo manual, solo aplicamos el estado actual
  }
}
// --- Setup y Loop ---
void fanSetup() {
  pinMode(PIN_RELE_FAN, OUTPUT);
  apagarVentilador(); // Apagar al inicio
  // Iniciar WiFi, NTP, etc.
}

