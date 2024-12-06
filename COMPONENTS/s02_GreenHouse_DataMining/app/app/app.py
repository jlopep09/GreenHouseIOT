import reflex as rx
from rxconfig import config
from app.pages.index import index
from app.pages.reads_list import reads_list
from app.pages.temps import temps_page


app = rx.App(
    theme=rx.theme(
        appearance="inherit",
        has_background=True,
        radius="medium",
        accent_color="jade",
    )
)

app.add_page(index, route="/")
app.add_page(reads_list, route="/reads")
app.add_page(temps_page, route="/temp")