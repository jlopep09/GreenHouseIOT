from typing import List
import requests
import reflex as rx
from datetime import datetime, timedelta
from app.backend.models.models import Greenhouse


class DataQueryGH(rx.State):

    api_response: str = "Cargando..."
    _greenhouses_list: rx.Field[List[Greenhouse]] =rx.field([])  # Atributo adicional para almacenar solo los nombres
    selected_gh_index: int = 0
    testint: int = 2
    @rx.var
    def is_gh_selected(self)->bool:
        return self.selected_gh_index!=0
    @rx.var
    def greenhouses_list(self) -> List[Greenhouse]:
        return self._greenhouses_list
    @rx.var
    def get_selected_gh_name(self) -> str:
        for greenhouse in self._greenhouses_list:
            if greenhouse.gh_id == self.selected_gh_index:
                return greenhouse.name
        return ""
    @rx.var
    def get_selected_gh_id(self) -> str:
        for greenhouse in self._greenhouses_list:
            if greenhouse.gh_id == self.selected_gh_index:
                return str(greenhouse.gh_id)
        return ""
   
    @rx.var
    def get_selected_gh_desc(self) -> str:
        for greenhouse in self._greenhouses_list:
            if greenhouse.gh_id == self.selected_gh_index:
                return greenhouse.description
        return ""
    @rx.var
    def get_selected_gh_date(self) -> str:
        for greenhouse in self._greenhouses_list:
            if greenhouse.gh_id == self.selected_gh_index:
                return greenhouse.date
        return ""
    
    def fetch_data(self):
        print("Intentando hacer fetch")
        try:
            response = requests.get("http://data_processing:8002/db/gh/")
            response.raise_for_status()  # Lanza un error si la respuesta tiene un código de estado de error
            gh_list_data = response.json()
            self.greenhouses_list.clear()
            # Extraer solo los nombres de los invernaderos
            if "greenhouses" in gh_list_data and gh_list_data["greenhouses"]:
                for gh in gh_list_data["greenhouses"]:
                    new_gh = Greenhouse(
                        gh_id=gh["id"],
                        date=gh["date"],
                        name=gh["name"],
                        description=gh.get("description"),  # Usa .get() para manejar claves opcionales
                        image=gh.get("image"),
                        ip=gh.get("ip"),
                    )
                    self.greenhouses_list.append(new_gh)
                
                time_str = (datetime.now() + timedelta(hours=1)).strftime("%H:%M:%S")
                self.api_response = "Última actualización: "+time_str
            else:
                self.api_response = "No se han encontrado invernaderos conectados"
                
        except requests.exceptions.RequestException as e:
            self.api_response = "Error al conectar con el servicio de procesamiento de datos"

    def select_gh(self, index:int):
        # Actualiza la variable selected_gh_index con el índice del invernadero seleccionado
        self.selected_gh_index = index
        #self.api_response = (f"id del invernadero seleccionado: {self.selected_gh_index}")

    
    def set_text(self, texto:str):
        self.api_response = texto
    @rx.var
    def get_ghlist_size(self) -> int:
        return len(self.greenhouses_list)
        
    def create_greenhouse(self):
        print("Intentando crear un invernadero")
        # Datos de prueba para crear el invernadero
        date = datetime.now().strftime("%Y-%m-%d")
        name = "Test->"+datetime.now().strftime("%H:%M:%S")
        description = "Invernadero creado para pruebas"
        ip = "192.168.1.101"
        image = None
        
        try:
            # Crea el cuerpo de la solicitud con los datos proporcionados
            data = {
                "date": date,
                "name": name,
                "description": description,
                "image": image,
                "ip": ip
            }

            # Realiza la solicitud POST al endpoint de creación
            response = requests.post("http://data_processing:8002/db/gh/", json=data)
            response.raise_for_status()  # Lanza un error si la respuesta tiene un código de estado de error

            # Si la solicitud es exitosa, muestra el mensaje
            response_data = response.json()
            if "message" in response_data and "id" in response_data:
                #self.api_response = f"Greenhouse created successfully with ID {response_data['id']}"
                self.fetch_data()
            else:
                self.api_response = "Error desconocido al crear el invernadero"
                
        except requests.exceptions.RequestException as e:
            self.api_response = f"Error al conectar con el servicio de creación de invernadero: {e}"

            