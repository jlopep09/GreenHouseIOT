import reflex as rx
from app.components.navbar_link import navbar_link
from app.components.darkmode_togle import dark_mode_toggle

def app_name_section() -> rx.Component:
    return  rx.hstack(
                rx.image(
                    src="/favicon.ico",
                    width="2em",
                    height="auto",
                    border_radius="25%",
                ),
                rx.heading(
                    "Greenhouse IOT", size="7", weight="bold"
                ),
                align_items="center",
            )
def middle_section(mobile_mode:bool) -> rx.Component: 
    if mobile_mode:
        return rx.menu.root(
                        rx.menu.trigger(
                            rx.icon("menu", size=30)
                        ),
                        rx.menu.content(
                            rx.menu.item("Home"),
                            rx.menu.item("About"),
                            rx.menu.item("Github"),
                            rx.menu.item("Contact"),
                        ),
                        justify="end",
                    )
    return rx.hstack(
            navbar_link("Home", "/"),
            navbar_link("About", "/#"),
            navbar_link("Github", "/#"),
            navbar_link("Contact", "/#"),
            spacing="5",
        )
def profile_section() -> rx.Component: 
    return  rx.menu.root(
                rx.menu.trigger(
                    rx.icon_button(
                        rx.icon("user"),
                        size="2",
                        radius="full",
                    )
                ),
                rx.menu.content(
                    rx.menu.item("Settings"),
                    rx.menu.item("Help"),
                    rx.menu.separator(),
                    rx.menu.item("Log out"),
                ),
                justify="end",
            )
def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                app_name_section(),
                middle_section(False),
                rx.hstack(
                    dark_mode_toggle(),
                    margin_left="5.5em"
                )
                ,
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                app_name_section(),
                
                rx.hstack(
                    middle_section(True), 
                    dark_mode_toggle()
                )
                ,
                justify="between",
                align_items="center",
            ),
        ),
        padding="1em",
        width="100%",
        border_bottom=rx.color_mode_cond( 
            "1px solid #D3D3D3" , 
            "1px solid #555555"
        )
    )