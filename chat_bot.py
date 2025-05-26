"""
Creación de un chatbot con Python y Flet. Uso de varias Apis.
"""

import flet
from flet import Page, TextField, ElevatedButton, Column, Text, Colors, Dropdown, dropdown, Container
from functions import get_response_ai, get_weather, get_pokemon, get_country_info

def main(page: Page):
    page.title = "Chatbot con Flet"
    page.window.width = 800
    page.window.height = 600
    page.bgcolor = Colors.WHITE
    # page.theme_mode = "dark"
    input_box = TextField(
        label="Escribe tu mensaje.",
        border_color=Colors.BLUE_200,
        focused_border_color=Colors.BLUE_600,
        text_style=flet.TextStyle(color=Colors.BLACK),
        expand=True # se expanda cuando el ancho del texto sea más grande
    )
    
    # Dropdown para seleccionar el modo de chat
    mode_dropdown = Dropdown(
        options=[
            dropdown.Option("chat", "Chat con IA"),
            dropdown.Option("tiempo", "Consultar Clima"),
            dropdown.Option("pokemon", "Consultar un Pokemón"),
            dropdown.Option("paises", "Consultar un País")
        ], 
        value="chat", # valor por defecto de la lista options
        label="modo",
        border_color=Colors.BLUE_200,
        color=Colors.BLACK
    )

    # Cambiar el texto del input dependiendo del modo seleccionado
    def on_mode_change(event):
        mode = mode_dropdown.value
        match mode:
            case "chat": input_box.label = "Escribe tu mensaje."
            case "tiempo": input_box.label = "Escribe una ciudad. Ejemplo: Madrid."
            case "pokemon": input_box.label = "Escribe el nombre de un Pokémon. Ejemplo: Pikachu."
            case "paises": input_box.label = "Escribe el nombre de un Pais. Ejemplo: España."
        page.update()

    # Cambiar el texto del input dependiendo del modo seleccionado
    mode_dropdown.on_change = on_mode_change

    # Área de chat
    chat_area = Column(scroll="auto", expand=True)

    # Flujo de mensajes usuario y chatbot
    def send_message(event):
        user_message = input_box.value
        if not user_message:
            return # si no hay mensaje, no hacemos nada y salimos de la función
        
        # Mostrar mensaje del usuario
        chat_area.controls.append(
            flet.Text(
                spans=[
                    flet.TextSpan("Usuario: ", style=flet.TextStyle(weight=flet.FontWeight.BOLD)),
                    flet.TextSpan(user_message)
                ]
            )
        )
        user_message = user_message.lower()

        # Aquí puedes añadir la lógica para el chatbot ejemplo, puedes usar una API de chatbot o un modelo de lenguaje
        if mode_dropdown.value == "tiempo":
            response = get_weather(user_message)
        elif mode_dropdown.value == "pokemon":
            response = get_pokemon(user_message)
        elif mode_dropdown.value == "paises":
            response = get_country_info(user_message)
        else:
            response = get_response_ai(user_message)

        # Mostrar respuesta
        chat_area.controls.append(
            flet.Text(
                spans=[
                    flet.TextSpan("ChatBot: ", style=flet.TextStyle(weight=flet.FontWeight.BOLD)),
                    flet.TextSpan(response)
                ]
            )
        )
        
        # Limpiar y actualizar
        input_box.value = ""
        page.update()

    send_button = ElevatedButton(text="Enviar", 
                                 on_click=send_message,
                                 bgcolor=Colors.BLUE_400,
                                 color=Colors.BLACK)
    
    chat_container = Container(
        content=chat_area,
        # bgcolor=Colors.WHITE,
        padding=10,
        border_radius=10,
        expand=True
    )

    input_container = Container(
        content=flet.Row(
            controls=[
                mode_dropdown,
                input_box,
                send_button
            ],
            spacing=10
        )
    )

    page.add(chat_container, input_container)
    page.update()

flet.app(target=main)