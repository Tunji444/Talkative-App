from uuid import uuid4
from nicegui import ui

messages = []

@ui.refreshable
def chat_messages(own_id):
    for user_id, avatar, text in messages:
        ui.chat_message(
            name="Gaem",
            stamp="now",
            avatar=avatar,
            text=text,
            sent=user_id == own_id
        )

@ui.page('/')
def index():
    def send():
        messages.append((user, avatar, text.value))
        chat_messages.refresh()
        text.value = ''

    user = str(uuid4())
    avatar = f"https://robohash.org/{user}?bgset=bg2"

   
    # with ui.column().classes('w-full h-screen justify-center items-center'):
    #     ui.image('images/logo.png').classes('rounded-xl shadow-lg')

    # Chat messages below
    with ui.column().classes('w-full items-stretch'):
        chat_messages(user)

    # Footer input
    with ui.footer().classes('bg-white'):
        with ui.row().classes('w-full items-center'):
            with ui.avatar():
                ui.image(avatar)
            text = (
                ui.input(placeholder='message')
                .props('rounded outlined')
                .classes('flex-grow')
                .on('keydown.enter', send)
            )

ui.run()