from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings


kb = KeyBindings()

@kb.add("enter")
def _(event):
    buffer = event.current_buffer

    document = buffer.document

    current_line = (
        document.current_line
    )

    # Empty line -> send
    if current_line == "":
        buffer.validate_and_handle()
        return

    # Otherwise create a new line
    buffer.insert_text("\n")

def get_input():
    text = prompt(
        "You (empty line to send):\n",
        multiline=True,
        key_bindings=kb
    )

    return text.strip()