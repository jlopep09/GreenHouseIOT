import reflex as rx
from app.pages.reads_list import TableReadsState
from app.views.navbar import navbar
from app.views.footer import footer
from app.backend.data_query import DataQueryGH
import plotly.express as px
# Crear un DataFrame con los datos
import pandas as pd


def temps_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.vstack(
           rx.center( rx.heading("Invernadero "+DataQueryGH.get_selected_gh_name, as_="h2", size="4", on_mount=TableReadsState.fetch_data), width="100%"),
           rx.center(get_temps_table(), width="100%"),
           rx.center(get_humidity_table(), width="100%"),
           rx.text(TableReadsState.api_response_reads, align="center", width = "100%"),
           min_height="85vh",width="100%"),
           
        footer()
    )

class PlotlyTempsState(TableReadsState):
    _df: pd.DataFrame = pd.DataFrame({
            "Fechas": [""],
            "Valores": [0],
        })
    fig = px.line(
        _df,
        x="Fechas",
        y="Valores",
        title="Evolución de la temperatura a lo largo del tiempo",
        labels={"Fecha": "Fechas", "Valores": "Temperatura"},
    )
    @rx.var
    def set_df(self):
        self._df = pd.DataFrame({
            "Fechas": self.dates_data,
            "Valores": self.temp_data,
        })
    @rx.event
    def update_temps_chart(self):
        self._df = pd.DataFrame({
            "Fechas": self.dates_data,
            "Valores": self.temp_data,
        })
        self.fig = px.line(
            self._df,
            x="Fechas",
            y="Valores",
            title="Evolución de la temperatura a lo largo del tiempo",
            labels={"Fecha": "Fechas", "Valores": "Temperatura"},
        )
class PlotlyHumidityState(TableReadsState):
    _df: pd.DataFrame = pd.DataFrame({
            "Fechas": [""],
            "Valores": [0],
        })
    fig = px.line(
        _df,
        x="Fechas",
        y="Valores",
        title="Evolución de la humedad a lo largo del tiempo",
        labels={"Fecha": "Fechas", "Valores": "Humedad"},
    )
    @rx.var
    def set_df(self):
        self._df = pd.DataFrame({
            "Fechas": self.dates_data,
            "Valores": self.humidity_data,
        })
    @rx.event
    def update_humidity_chart(self):
        self._df = pd.DataFrame({
            "Fechas": self.dates_data,
            "Valores": self.humidity_data,
        })
        self.fig = px.line(
            self._df,
            x="Fechas",
            y="Valores",
            title="Evolución de la humedad a lo largo del tiempo",
            labels={"Fecha": "Fechas", "Valores": "Humedad"},
        )

def get_temps_table() -> rx.Component:
    return rx.vstack(
        rx.plotly(data=PlotlyTempsState.fig),
        on_mount=PlotlyTempsState.update_temps_chart
    )
def get_humidity_table() -> rx.Component:
    return rx.vstack(
        rx.plotly(data=PlotlyHumidityState.fig),
        on_mount=PlotlyHumidityState.update_humidity_chart
    )


            