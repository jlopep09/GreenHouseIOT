import reflex as rx
from app.pages.reads_list import TableReadsState
from app.views.navbar import navbar
from app.views.footer import footer
from app.backend.data_query import DataQueryGH


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
        rx.text("Hola")
    )


            