import reflex as rx
from app.components.navbar_link import navbar_link
from app.components.darkmode_togle import dark_mode_toggle



def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
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
                ),
                rx.hstack(
                    navbar_link("Home", "/"),
                    navbar_link("About", "/#"),
                    navbar_link("Github", "/#"),
                    navbar_link("Contact", "/#"),
                    spacing="5",
                ),
                rx.hstack(
                    dark_mode_toggle(),
                    rx.menu.root(
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
                    ),
                    margin_left="5.5em"
                )
                ,
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
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
                ),
                rx.hstack(
                    rx.menu.root(
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
                    ), 
                    dark_mode_toggle(),
                    rx.menu.root(
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
                )
                ,
                justify="between",
                align_items="center",
            ),
        ),
        # bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
        border_bottom=rx.color_mode_cond( 
            "1px solid #D3D3D3" , 
            "1px solid #555555"
        )
    )