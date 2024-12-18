import reflex as rx
from app.backend.data_query import DataQueryGH
from app.backend.models.models import Greenhouse

from reflex import State

class FilterState(State):
    sort_order: str = "asc"
    
    @rx.event
    def change_value(self, value: str):
        self.sort_order = value

def gh_button(gh):
    # Obtener el índice del invernadero
    #index_gh = DataQueryGH.get_id_by_name(greenhouse_name)
    
    return rx.button(
        gh.name,
        width="60%",
        on_click= DataQueryGH.select_gh(gh.gh_id)  # Pasar el índice correctamente
    )


def get_gh_stack():

    return rx.cond(
        DataQueryGH.get_ghlist_size <= 0,  # Verifica si la lista está vacía
        rx.text("No hay invernaderos disponibles"),  # Si está vacía
        rx.vstack(
            
            rx.cond(
                FilterState.sort_order == "desc",
                rx.foreach(DataQueryGH.greenhouses_sorted_desc_list, gh_button),
                rx.foreach(DataQueryGH.greenhouses_sorted_asc_list, gh_button)
            ),
            spacing="4",
            align_items="center",
            width="100%",
        )  # Si no está vacía
    )

