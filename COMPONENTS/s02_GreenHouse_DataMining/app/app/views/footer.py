import reflex as rx
class FooterState(rx.State):
    
    home_url:str = "/"
    about_url:str = "/about"
    github_url:str = "https://github.com/jlopep09/GreenHouseIOT"
    contact_url:str = "/contact"
    policy_url:str = "/policy"
    terms_url:str = "/terms"

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

def footer_item(text: str, href: str, external:bool = False) -> rx.Component:
    return rx.link(rx.text(text, size="3"), href=href, is_external=external)


def footer_items_1() -> rx.Component:
    return rx.flex(
        rx.heading(
            "PRODUCTS", size="4", weight="bold", as_="h3"
        ),
        footer_item("Greenhouse IOT", FooterState.about_url),
        footer_item("Repository", FooterState.github_url, external = True),
        spacing="4",
        text_align=["center", "center", "start"],
        flex_direction="column",
    )


def footer_items_2() -> rx.Component:
    return rx.flex(
        rx.heading(
            "ABOUT US", size="4", weight="bold", as_="h3"
        ),
        footer_item("Contact Us", FooterState.contact_url),
        footer_item("Our Team", FooterState.about_url),
        spacing="4",
        text_align=["center", "center", "start"],
        flex_direction="column",
    )


def footer_items_3() -> rx.Component:
    return rx.flex(
        rx.heading(
            "RESOURCES", size="4", weight="bold", as_="h3"
        ),
        footer_item("Privacy Policy", FooterState.policy_url),
        footer_item("Terms of Service", FooterState.terms_url),
        spacing="4",
        text_align=["center", "center", "start"],
        flex_direction="column",
    )


def social_link(icon: str, href: str, external:bool = False) -> rx.Component:
    return rx.link(rx.icon(icon), href=href, is_external=external)


def socials() -> rx.Component:
    return rx.flex(
        social_link("instagram", FooterState.contact_url),
        social_link("twitter", FooterState.contact_url),
        social_link("github", FooterState.github_url, external=True),
        social_link("mail", "mailto:jlopep09@estudiantes.unileon.es"),
        spacing="3",
        justify_content=["center", "center", "end"],
        width="100%",
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.vstack(
            rx.divider(),
            rx.flex(
                footer_items_1(),
                footer_items_2(),
                footer_items_3(),
                justify="between",
                spacing="6",
                flex_direction=["column", "column", "row"],
                width="100%",
            ),
            rx.divider(),
            rx.flex(
                rx.hstack(
                    rx.image(
                        src="/favicon.ico",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.text(
                        "2024 - José Antonio López",
                        size="3",
                        white_space="nowrap",
                        weight="medium",
                    ),
                    spacing="2",
                    align="center",
                    justify_content=[
                        "center",
                        "center",
                        "start",
                    ],
                    width="100%",
                ),
                socials(),
                spacing="4",
                flex_direction=["column", "column", "row"],
                width="100%",
            ),
            spacing="5",
            width="100%",
        ),
        width="100%",
        padding = "20px"
    )