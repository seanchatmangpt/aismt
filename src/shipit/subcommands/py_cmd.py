import asyncio

import typer
import pyperclip

from utils.create_prompts import create_python

app = typer.Typer(help="Advanced Python Assistant")


@app.command("bot")
def update_python_code(
    paste_code: bool = typer.Option(False, "--paste", "-p", help="Paste code to update")
):
    if paste_code:
        print(pyperclip.paste())
        user_input = typer.prompt("How would you like this code updated?")
        user_input = pyperclip.paste() + "\n\nUser: I would like to have " + user_input
    else:
        user_input = typer.prompt("What would you like for me to generate?")

    asyncio.run(_update_python_code(user_input))


async def _update_python_code(user_input):
    code = user_input

    code = await create_python(prompt=code)

    # Display code snippet details and ask for confirmation
    confirmed = False
    while not confirmed:
        print(f"Code Snippet Details:\n{code}")

        confirm = typer.prompt("Are these details correct? [y/N]")
        if confirm.lower() in ["y", "yes"]:
            confirmed = True
        else:
            # Re-prompt for details
            code = await create_python(prompt=code)

    pyperclip.copy(code)
    print(f"Code copied to clipboard.")
