import reflex as rx
from app.components.card_img import get_img_elem
from app.backend.data_query import DataQueryGH
from app.pages.reads_list import TableReadsState


class ReadsState(rx.State):
    # Función para redirigir a la subpágina con un parámetro
    reads_list_url:str = "/reads"
    @rx.event
    def go_to_reads_list(self):
        return rx.redirect(self.reads_list_url, external=False)

def content_card_info() -> rx.Component:
    return rx.vstack(
            rx.separator(),
            rx.heading("Selección", as_="h3",width = "100%", text_align = "center", padding_y= "0.6em", size="4"),
            get_division("/greenhouse.svg",main_variant=True),
            rx.separator(),
            rx.heading("Agua", as_="h3",width = "100%", text_align = "center", padding_y= "0.6em", size="4"),
            get_division("/glass-of-water.svg",switch_variant=False),
        height="100%", 
        width = "100%",
        spacing="0",
    )

def get_division(img_url:str,main_variant: bool=False, switch_variant: bool= False) -> rx.Component:
    return rx.hstack(
        rx.vstack(
            get_img_elem(img_url),
            height="100%", 
            width = "50%",),
        rx.cond(not main_variant,
            rx.vstack(
                
                rx.cond(switch_variant,
                    rx.flex(rx.switch(),width = "60%", height = "50px", background_color = "gray", justify="center", align="center", border_radius = "5px"),
                    popup_water_now()
                ),
                getDialog(),
                rx.text(TableReadsState.get_last_humidity_data, align="center", size="3"),
                height="100%", 
                width = "50%",
                justify="center",
                align="center",
                spacing="3",
                padding_left="2em",
            ),
            rx.vstack(
                    rx.center(
                        rx.heading(rx.text("Invernadero", align="center", text_decoration = "underline"), as_="h3",width = "100%", text_align = "left", padding_bottom= "0.5em", size="4", padding_x = "0.5em"),
                        rx.text(DataQueryGH.get_selected_gh_name, width = "100%", text_align = "center", padding_left="0em"  ),
                        rx.text(DataQueryGH.get_selected_gh_desc, width = "100%", text_align = "center", padding_left="0em"  ),
                        rx.text(DataQueryGH.get_selected_gh_date, width = "100%", text_align = "center", padding_left="0em", padding_bottom = "1em"  ),
                        rx.cond(
                            DataQueryGH.is_gh_selected,
                            rx.button("Mostrar Lecturas",on_click=lambda: ReadsState.go_to_reads_list()),
                            rx.button("Mostrar Lecturas",disabled=True),
                        ),
                        width = "100%",
                        direction="column"
                    ),
                    height="100%", 
                    width = "50%",
                    justify="center",
                    spacing="0",
                    padding_left="2em",
                    ),
                
            
        ),
        height="40%", 
        width = "100%",
        
    )
def getDialog() -> rx.Component:
    return rx.dialog.root(
            rx.cond(
                    DataQueryGH.is_gh_selected,
                    rx.dialog.trigger(rx.button(rx.icon("clock"), width = "60%", height = "50px")),
                    rx.dialog.trigger(rx.button(rx.icon("clock"), width = "60%", height = "50px", disabled=True))
                ),
            rx.dialog.content(
                rx.dialog.title("Programación de riego"),
                rx.dialog.description(
                    "Debes introducir el valor porcentual mínimo de humedad deseado sin decimales, el sistema sumistrará agua hasta superar dicho valor. Ejemplo: 30",
                    size="2",
                    margin_bottom="16px",
                ),
                rx.flex(
                    rx.text(
                        "Porcentaje mínimo de humedad",
                        as_="div",
                        size="2",
                        margin_bottom="4px",
                        weight="bold",
                    ),
                    rx.input(
                        default_value="10",
                        placeholder="Introduzca el porcentaje de humedad deseado",
                    ),
                    direction="column",
                    spacing="3",
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            color_scheme="gray",
                            variant="soft",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button("Save"),
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
            ),
        ),
def popup_water_now() -> rx.Component:
    return rx.alert_dialog.root(
        rx.cond(
                    DataQueryGH.is_gh_selected,
                    rx.alert_dialog.trigger(rx.button(rx.icon("droplet"), width = "60%", height = "50px")),
                    rx.alert_dialog.trigger(rx.button(rx.icon("droplet"), width = "60%", height = "50px", disabled=True))
                ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Suministrar agua"),
            rx.alert_dialog.description(
                "¿Estás seguro de que quieres suministrar agua ahora? Se recomienda programar el suministro estableciendo una humedad mínima.",
                size="2",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Suministrar",
                        color_scheme="red",
                        variant="solid",
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
    )