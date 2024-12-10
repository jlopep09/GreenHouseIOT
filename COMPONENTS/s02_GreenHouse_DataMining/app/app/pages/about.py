import reflex as rx
from app.pages.reads_list import TableReadsState
from app.views.navbar import navbar
from app.views.footer import footer
from app.backend.data_query import DataQueryGH


def about_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.center(
                rx.heading("Sobre nosotros", as_="h2", size="6", margin_y = "40px"),
                width="100%",
            ),
            rx.center(
                rx.image(
                    src="https://www.chemicalsafetyfacts.org/wp-content/uploads/shutterstock_609086588-scaled-1-800x400.jpg",  # Sustituye por tu enlace de imagen de Google
                    alt="Imagen principal",
                    width="800px",
                    height="400px",
                ),
                width="100%",
            ),
            rx.center(
                get_content(),
                width="100%",
            ),
            height="85vh",
            width="100%",
        ),
        footer(),
    )


def get_content() -> rx.Component:
    return rx.vstack(
        rx.text("Greenhouse iot es un proyecto desarrollado durante las prácticas en la empresa CDS."),
        rx.text("El proyecto nace de la necesidad de controlar el crecimiento de plantas haciendo uso de sensores para obtener datos necesarios para un óptimo cuidado."),
        rx.text("En esta primera versión el sistema permite controlar luces pero en un futuro será posible el control de ventilación, calefacción y riego.")
    )
