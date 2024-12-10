import reflex as rx
from app.pages.reads_list import TableReadsState
from app.views.navbar import navbar
from app.views.footer import footer
from app.backend.data_query import DataQueryGH

terms_of_service = """
TÉRMINOS DE SERVICIO

Bienvenido a GreenhouseIOT. Al usar esta aplicación, aceptas los siguientes términos y condiciones. Por favor, léelos detenidamente antes de utilizarla.

1. USO DE LA APLICACIÓN
   Esta aplicación está diseñada para ejecutarse en un entorno local y proporcionar las funcionalidades descritas en su documentación. Al usarla, te comprometes a no utilizarla con fines ilegales, fraudulentos o que puedan causar daño a terceros o al software.

2. PROPIEDAD INTELECTUAL
   Todos los derechos relacionados con el software, incluidos los textos, gráficos, logos, y código fuente, son propiedad exclusiva de GreenhouseIOT. Queda prohibida la copia, distribución, modificación o uso no autorizado del software sin el consentimiento expreso del propietario.

3. EXCLUSIÓN DE RESPONSABILIDADES
   Esta aplicación se proporciona "tal cual", sin garantías de ningún tipo, ya sean explícitas o implícitas. GreenhouseIOT no se responsabiliza de:
   - Pérdida de datos debido a mal uso o fallos del sistema.
   - Daños directos o indirectos derivados del uso de la aplicación.
   - Problemas de compatibilidad con sistemas o configuraciones específicas.

4. PRIVACIDAD
   La aplicación no recopila ni almacena información personal ni transfiere datos a terceros. Toda la información procesada permanece en el dispositivo o infraestructura local del usuario.

5. MODIFICACIONES Y ACTUALIZACIONES
   GreenhouseIOT se reserva el derecho de modificar o actualizar estos términos en cualquier momento. Se recomienda a los usuarios revisar los términos periódicamente para estar al tanto de posibles cambios.

6. SOPORTE Y CONTACTO
   Para preguntas o problemas relacionados con la aplicación, puedes contactarnos a través de jlopep09@estudiantes.unileon.es

Al instalar y utilizar esta aplicación, confirmas que has leído, entendido y aceptado estos términos de servicio.
"""

def terms_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.vstack(
           rx.center( rx.heading("Términos de servicio", as_="h2", size="6", margin_y = "40px"), width="100%"),
           rx.center(get_content(), width="100%"),
           height="85vh",width="100%"
        ),    
        footer()
    )
def get_content() -> rx.Component:
    return rx.vstack(
        rx.text(terms_of_service)
    )


            