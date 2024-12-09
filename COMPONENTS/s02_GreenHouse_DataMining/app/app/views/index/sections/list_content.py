import reflex as rx
from app.components.filter_select import filter_select_order, filter_select_lugar
from app.components.custom_buttons import get_gh_stack
from app.backend.data_query import DataQueryGH

def content_card_list() -> rx.Component:
    return rx.vstack(
            rx.separator(),
            rx.center(
                    rx.text("Ordenar:"),
                    filter_select_order(),
                    rx.text("Localización:"),
                    filter_select_lugar(),
                    rx.button(rx.icon("refresh-ccw"), on_click=DataQueryGH.fetch_data, on_mount=DataQueryGH.fetch_data),
                    width = "100%",
                    padding_bottom = "0.5em",
                    spacing="2"
            ),
            get_gh_stack(),
            #rx.button(rx.icon("circle-plus"), on_click=DataQueryGH.create_greenhouse),
            rx.text(DataQueryGH.api_response),

            
            
            height="100%", 
            width = "100%",
            align="center",
        )