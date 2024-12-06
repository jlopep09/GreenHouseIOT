import reflex as rx

def filter_select_order() -> rx.Component:
    return rx.select.root(
        rx.select.trigger(),
        rx.select.content(
            rx.select.group(
                rx.select.label("Tipo de orden"),
                rx.select.separator(),
                rx.select.item("Por defecto", value="default"),
                rx.select.item("Nombre", value="name"),
                rx.select.item("Fecha", value="date"),
            ),
        ),
        default_value="default",
    )
def filter_select_lugar() -> rx.Component:
    return rx.select.root(
        rx.select.trigger(),
        rx.select.content(
            rx.select.group(
                rx.select.label("Filtrar por localización"),
                rx.select.separator(),
                rx.select.item("Cualquiera", value="default"),
                rx.select.item("León", value="leon"),
                rx.select.item("Ponferrada", value="ponferrada"),
                rx.select.item("Madrid", value="madrid"),
            ),
        ),
        default_value="default",
    )