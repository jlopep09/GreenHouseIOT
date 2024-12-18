import reflex as rx
from app.components.custom_buttons import FilterState
from app.backend.data_query import DataQueryGH

def filter_select_order() -> rx.Component:
    return rx.select.root(
        rx.select.trigger(),
        rx.select.content(
            rx.select.group(
                rx.select.label("Tipo de orden"),
                rx.select.separator(),
                rx.select.item("Por defecto", value="default"),
                rx.select.item("Ascendente", value="asc"),
                rx.select.item("Descendente", value="desc"),
            ),
        ),
        default_value="default",
        on_change=FilterState.change_value
    )
def filter_select_lugar() -> rx.Component:
    return rx.select.root(
        rx.select.trigger(),
        rx.select.content(
            rx.select.group(
                rx.select.label("Filtrar por localización"),
                rx.select.separator(),
                rx.select.item("Cualquiera", value="all"),
                rx.select.item("León", value="leon"),
                rx.select.item("Ponferrada", value="ponferrada"),
                rx.select.item("Madrid", value="madrid"),
            ),
        ),
        default_value="all",
        on_change=DataQueryGH.change_city_value
    )