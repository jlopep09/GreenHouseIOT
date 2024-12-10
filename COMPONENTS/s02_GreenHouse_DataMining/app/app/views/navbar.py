import reflex as rx
from app.components.darkmode_togle import dark_mode_toggle

class NavbarState(rx.State):
    
    home_url:str = "/"
    about_url:str = "/about"
    github_url:str = "https://github.com/jlopep09/GreenHouseIOT"
    contact_url:str = "/contact"

    @rx.event
    def go_to_home(self):
        return rx.redirect(self.home_url, external=False)
    @rx.event
    def go_to_about(self):
        return rx.redirect(self.about_url, external=False)
    @rx.event
    def go_to_github(self):
        return rx.redirect(self.github_url, external=True)
    @rx.event
    def go_to_contact(self):
        return rx.redirect(self.contact_url, external=False)

def app_name_section() -> rx.Component:
    return  rx.hstack(
                rx.image(
                    src="/favicon.ico",
                    width="2em",
                    height="auto",
                    border_radius="25%",
                ),
                rx.heading(
                    "Greenhouse IOT", size="7", weight="bold",cursor="pointer",on_click=lambda: NavbarState.go_to_home()
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
                            rx.menu.item("Home",cursor="pointer",on_click=lambda: NavbarState.go_to_home()),
                            rx.menu.item("About",cursor="pointer",on_click=lambda: NavbarState.go_to_about()),
                            rx.menu.item("Github",cursor="pointer",on_click=lambda: NavbarState.go_to_github()),
                            rx.menu.item("Contact",cursor="pointer",on_click=lambda: NavbarState.go_to_contact()),
                        ),
                        justify="end",
                    )
    return rx.hstack(
            rx.link(rx.text("Home", size="4", weight="medium"), href=NavbarState.home_url, is_external=False),
            rx.link(rx.text("About", size="4", weight="medium"), href=NavbarState.about_url, is_external=False),
            rx.link(rx.text("Github", size="4", weight="medium"), href=NavbarState.github_url, is_external=True),
            rx.link(rx.text("Contact", size="4", weight="medium"), href=NavbarState.contact_url, is_external=False),
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