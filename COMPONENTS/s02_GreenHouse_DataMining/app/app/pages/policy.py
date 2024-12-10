import reflex as rx
from app.pages.reads_list import TableReadsState
from app.views.navbar import navbar
from app.views.footer import footer
from app.backend.data_query import DataQueryGH


def policy_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.vstack(
           rx.center( rx.heading("Política de privacidad", as_="h2", size="6", margin_y = "40px"), width="100%"),
           rx.center(get_content(), width="100%"),
           height="85vh",width="100%"
        ),    
        footer()
    )
def get_content() -> rx.Component:
    return rx.vstack(
        rx.text("En GreenhouseIOT, valoramos tu privacidad y nos comprometemos a proteger cualquier información personal que compartas con nosotros. Sin embargo, es importante destacar que nuestra aplicación no recopila ni almacena ningún tipo de información personal o datos del usuario en servidores externos ni en la nube."),
        rx.heading("Alcance de la recopilación de datos", as_="h3", size="4", margin_y = "20px"),
        rx.text("Nuestra aplicación se ejecuta completamente en un entorno local, utilizando una base de datos local que no se conecta a internet ni transfiere datos a terceros. Toda la información procesada en la aplicación permanece en tu dispositivo o infraestructura local."),
        rx.heading("Datos que no recopilamos", as_="h3", size="4", margin_y = "20px"),
        rx.text("Información personal, como nombre, correo electrónico, dirección, número de teléfono, etc. Información de uso o interacción con la aplicación. Datos de localización o cualquier otro tipo de información identificativa."),
        rx.heading("Seguridad de los datos", as_="h3", size="4", margin_y = "20px"),
        rx.text("Aunque nuestra aplicación no recopila información personal, recomendamos proteger tu dispositivo y red local para garantizar la seguridad de la información almacenada en tu sistema."),
        rx.heading("Actualizaciones de la política de privacidad", as_="h3", size="4", margin_y = "20px"),
        rx.text("Nos reservamos el derecho de actualizar esta política en caso de que cambie la funcionalidad de la aplicación. Cualquier cambio será comunicado dentro de la aplicación.Si tienes alguna pregunta sobre esta política, no dudes en ponerte en contacto con nosotros a través de jlopep09@estudiantes.unileon.es"),
    )


            