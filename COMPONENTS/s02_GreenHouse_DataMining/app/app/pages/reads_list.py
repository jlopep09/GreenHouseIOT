from typing import List
import reflex as rx
import requests
from app.views.navbar import navbar
from app.views.footer import footer
from app.backend.data_query import DataQueryGH
from app.backend.models.models import Sensor_entry

class TableReadsState(DataQueryGH):
    api_response_reads:str = "Buscando lecturas..."
    columns: List[str] = ["id", "moist", "humidity", "water level", "temperature", "light", "date"]
    _reads_list: rx.Field[List[Sensor_entry]] = rx.field([])
    table_gh :str = "0"
    api_url :str = "http://data_processing:8002/db/reads/"
    
    @rx.var
    def get_api_url(self) -> str:
        return self.api_url + str(self.selected_gh_index)
    @rx.var
    def reads_list(self) -> List[Sensor_entry]:
        return self._reads_list
    
    @rx.var
    def table_data(self) -> List[List[str]]:
        # Filtra por gh_id igual a DataQueryGH.selected_gh_index
        return [
            [
                str(entry.read_id),
                str(entry.moist),
                str(entry.humidity),
                str(entry.water_level),
                str(entry.temperature),
                "On" if entry.light else "Off",  # Formatea el booleano como texto
                entry.date,
            ]
            for entry in self._reads_list
        ]
    @rx.var
    def temp_data(self) -> List[List[str]]:
        # Filtra por gh_id igual a DataQueryGH.selected_gh_index
        result = []
        for entry in self._reads_list:
            result.append(entry.temperature) 
        return result
    @rx.var
    def dates_data(self) -> List[List[str]]:
        # Filtra por gh_id igual a DataQueryGH.selected_gh_index
        result = []
        for entry in self._reads_list:
            result.append(entry.date) 
        return result

    def fetch_data(self):
        print("Intentando hacer fetch")
        
        # Capturar el valor actual de la variable reactiva
        id_req = ""  # Llama directamente al método
        
        

        try:
            # Construir la URL con el valor capturado
    
            response = requests.get(self.get_api_url)
            response.raise_for_status()
            reads_list_data = response.json()

            # Limpiar la lista actual
            self._reads_list.clear()

            # Procesar la respuesta
            if "reads" in reads_list_data and reads_list_data["reads"]:
                for rd in reads_list_data["reads"]:
                    new_rd = Sensor_entry(
                        read_id=rd["id"],
                        moist=rd["moist"],
                        humidity=rd["humidity"],
                        water_level=rd.get("water_level"),
                        temperature=rd.get("temperature"),
                        light=rd.get("light"),
                        date=rd["date"],
                        gh_id=rd["gh_id"],
                    )
                    self._reads_list.append(new_rd)
                self.api_response_reads = "Lecturas cargadas correctamente"
            else:
                self.api_response_reads = "No se han encontrado lecturas para el invernadero seleccionado"
        except requests.exceptions.RequestException as e:
            self.api_response_reads = f"Error al conectar con el servicio: {str(e)}"

def reads_list() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.vstack(
           rx.center( rx.heading("Invernadero "+DataQueryGH.get_selected_gh_name, as_="h2", size="4", on_mount=TableReadsState.fetch_data), width="100%"),
           get_table(),
           rx.text(TableReadsState.api_response_reads),
           height="85vh",width="100%"),
           
        footer()
    )

def get_table() -> rx.Component:
    return rx.data_table(
        data=TableReadsState.table_data,
        columns=TableReadsState.columns,
        
    )


            