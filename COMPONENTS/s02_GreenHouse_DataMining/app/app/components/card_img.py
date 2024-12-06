import reflex as rx

def get_img_elem(img_url: str) -> rx.Component:
    return rx.center(
            rx.image(
                src=img_url,
                width="55%", 
                height="auto",
                border_radius="15px",
                border="5px solid #555",
                 
               
            ),
        height = "100%",width = "100%",
    )