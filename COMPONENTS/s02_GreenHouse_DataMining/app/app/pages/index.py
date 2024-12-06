import reflex as rx
from app.views.navbar import navbar
from app.views.footer import footer
from app.views.index.index_card import section_card
from app.views.index.index_card import Section_name
from app.styles.index import sections_styles

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.desktop_only(get_grid(cols = 3, rows=1), width="100%"),
        rx.mobile_and_tablet(get_grid(cols = 1, rows=3), width="100%"),
        footer()
    )


def get_grid(cols: int, rows:int)-> rx.Component:
    return rx.grid(
        section_card(Section_name.GH_LIST),
        section_card(Section_name.GH_INFO),
        section_card(Section_name.GH_OPTIONS),
        columns= str(cols),
        rows=str(rows),
        **sections_styles         
    )              