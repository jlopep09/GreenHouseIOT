import reflex as rx
import asyncio

import requests
from app.backend.data_query import DataQueryGH
from app.components.card_img import get_img_elem
from enum import Enum
from app.pages.reads_list import TableReadsState
class TempState(rx.State):
    # Función para redirigir a la subpágina con un parámetro
    temp_page_url:str = "/temp"
    @rx.event
    def go_to_temp_page(self):
        return rx.redirect(self.temp_page_url, external=False)

class Variant(Enum):
    LIGHT = 0,
    TEMP = 1
class ImgState(rx.State):
    img_light_url: str = "/light-bulb-off.svg"
    is_on: bool = False
    state_str:str = "no changes"
    @rx.var
    def turnOn(self):
        self.is_on = True
        self.img_light_url = "/light-bulb-on.svg"
        
    @rx.var
    def turnOff(self):
        self.is_on = False
        self.img_light_url = "/light-bulb-off.svg"
        
    @rx.var
    def getImg(self):
        if self.is_on:
            self.img_light_url = "/light-bulb-on.svg"
        else:
            self.img_light_url = "/light-bulb-off.svg"
        return self.img_light_url
    @rx.event
    def switchState(self, value:bool):
        
        if value:
            self.turnOn
            self.state_str = self.is_on
        else:
            self.turnOff
            self.state_str = self.is_on
        
def content_card_options() -> rx.Component:
    return rx.vstack(
            rx.separator(),
            rx.heading("Luz", as_="h3",width = "100%", text_align = "center", padding_y= "0.6em", size="4"),
            #rx.heading(ImgState.getImg, as_="h3",width = "100%", text_align = "center", padding_y= "0.6em", size="4"),
            get_division(ImgState.img_light_url,Variant.LIGHT),

            rx.separator(),
            rx.heading("Temperatura", as_="h3",width = "100%", text_align = "center", padding_y= "0.6em", size="4"),
            get_division("/temperature.svg",Variant.TEMP, icon_1="arrow-up-narrow-wide"),

        height="100%", 
        width = "100%",
        spacing="0",
        )

class SendConfigState(DataQueryGH):
    api_text: str = ""
    @rx.event
    def send_time_data(self, form_data: dict):
        try:
            self.api_text = "Enviando datos..."
            timer_on = form_data["timer_on"]
            timer_off = form_data["timer_off"]
            
            send_url_on = "http://192.168.1.37/light/on/"
            send_url_off = "http://192.168.1.37/light/off/"
            
            response = requests.post(send_url_on, data={"time": timer_on}, timeout=5)
            response = requests.post(send_url_off, data={"time": timer_off}, timeout=5)

            response.raise_for_status()  # Lanza un error si la respuesta tiene un código de estado de error
            self.api_text = f"Las luces han sido programadas correctamente"
        except Exception as exc:
            self.api_text = f"Error al obtener los datos del formulario: {exc}"

def get_division(img_url:str, variant: Variant, icon_1: str = "clock") -> rx.Component:
    return rx.hstack(
        rx.vstack(
            get_img_elem(img_url),
            
            height="100%", 
            width = "50%",),
        rx.vstack(
            
            rx.cond(variant == Variant.LIGHT,
                rx.flex(rx.switch(on_change = ImgState.switchState, default_checked=ImgState.is_on),width = "60%", height = "50px", background_color = "gray", justify="center", align="center", border_radius = "5px"),
                rx.cond(
                    DataQueryGH.is_gh_selected,
                    rx.button(rx.icon(icon_1),on_click=lambda: TempState.go_to_temp_page(), width = "60%", height = "50px"),
                    rx.button(rx.icon(icon_1), width = "60%", height = "50px",disabled=True),
                )                  
            ),
            getDialog(variant),
            rx.cond(variant== Variant.TEMP,
                rx.text(TableReadsState.get_last_temp_data, align="center", size="3")
            ),
            height="100%", 
            width = "50%",
            justify="center",
            align="center",
            spacing="3",
            padding_left="2em",
        ),  
    height="40%", 
    width = "100%",
)
def getDialog(variant = Variant) -> rx.Component:
    return rx.cond(variant == Variant.LIGHT,
        rx.dialog.root(
            rx.cond(
                    DataQueryGH.is_gh_selected,
                    rx.dialog.trigger(rx.button(rx.icon("clock"), width = "60%", height = "50px")),
                    rx.dialog.trigger(rx.button(rx.icon("clock"), width = "60%", height = "50px", disabled=True))
                ),
            rx.dialog.content(
                rx.dialog.title("Programación de luces"),
                rx.dialog.description(
                    "Debes usar el formato HH:MM para un correcto funcionamiento. Ejemplo: 09:30",
                    size="2",
                    margin_bottom="16px",
                ),
                rx.form(
                    rx.flex(
                        rx.text(
                            "Hora de encendido",
                            as_="div",
                            size="2",
                            margin_bottom="4px",
                            weight="bold",
                        ),
                        rx.input(
                            default_value="09:00",
                            placeholder="Introduzca la hora de encendido deseada",
                            name = "timer_on"
                        ),
                        rx.text(
                            "Hora de apagado",
                            as_="div",
                            size="2",
                            margin_bottom="4px",
                            weight="bold",
                        ),
                        rx.input(
                            default_value="20:00",
                            placeholder="Introduzca la hora de apagado deseada",
                            name = "timer_off"
                        ),
                        rx.text(
                            SendConfigState.api_text
                        ),           
                        rx.flex(
                            rx.dialog.close(
                                rx.button(
                                    "Close",
                                    color_scheme="gray",
                                    variant="soft",
                                ),
                            ),
                            
                            rx.button("Save", type="submit"),
                            
                            spacing="3",
                            margin_top="16px",
                            justify="end"
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    on_submit=SendConfigState.send_time_data,
                    reset_on_submit=False,
                )

            ),
        ),
        rx.dialog.root(
            rx.cond(
                    DataQueryGH.is_gh_selected,
                    rx.dialog.trigger(rx.button(rx.icon("clock"), width = "60%", height = "50px")),
                    rx.dialog.trigger(rx.button(rx.icon("clock"), width = "60%", height = "50px", disabled=True))
                ),
            rx.dialog.content(
                rx.dialog.title("Programación de ventiladores y calentadores"),
                rx.dialog.description(
                    "Debes introducir las temperaturas objetivo sin decimales. Ejemplo: 27",
                    size="2",
                    margin_bottom="16px",
                ),
                rx.flex(
                    rx.text(
                        "Temperatura máxima",
                        as_="div",
                        size="2",
                        margin_bottom="4px",
                        weight="bold",
                    ),
                    rx.input(
                        default_value="32",
                        placeholder="Introduzca la temperatura máxima deseada",
                    ),
                    rx.text(
                        "Temperatura mínima",
                        as_="div",
                        size="2",
                        margin_bottom="4px",
                        weight="bold",
                    ),
                    rx.input(
                        default_value="18",
                        placeholder="Introduzca la temperatura mínima deseada",
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
    )

def getSuccessPopup(texto: str)-> rx.Component:
    return rx.toast.success(texto)

def getErrorPopup(texto: str)-> rx.Component:
    return rx.toast.error("Error:"+ texto)

def getInfoPopup(texto: str)-> rx.Component:
    return rx.toast.error(texto)


