import reflex as rx
from rxconfig import config
from app.pages.index import index
from app.pages.reads_list import reads_list
from app.pages.temps import temps_page
from app.pages.terms import terms_page
from app.pages.policy import policy_page
from app.pages.about import about_page
from app.pages.contact import contact_page


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
app.add_page(terms_page, route="/terms")
app.add_page(about_page, route="/about")
app.add_page(contact_page, route="/contact")
app.add_page(policy_page, route="/policy")