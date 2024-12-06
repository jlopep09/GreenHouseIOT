from enum import Enum
import reflex as rx
from app.views.index.sections.list_content import content_card_list
from app.views.index.sections.config_content import content_card_options
from app.views.index.sections.info_content import content_card_info


class Section_name(Enum):
    GH_LIST = "GH_LIST",
    GH_INFO= "GH_INFO",
    GH_OPTIONS= "GH_OPTIONS"

def section_card(section: Section_name)-> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(get_card_title(section), as_="h2",width = "100%", text_align = "center"),
            get_card_content(section),
            height="100%", width = "100%", padding = "0.5em"
        ),
        width="100%",
        height = "700px",
    )
def get_card_title(section: Section_name) -> str:
    match section:
        case Section_name.GH_INFO:
            return "INFORMACIÓN"
        case Section_name.GH_LIST:
            return "INVERNADEROS CONECTADOS"
        case _:
            return "AUTOMATIZACIÓN"


def get_card_content(section: Section_name) -> rx.Component:
    if section == Section_name.GH_INFO:
        return content_card_info()
    elif section == Section_name.GH_LIST:
        return content_card_list()
    else:
        return content_card_options()