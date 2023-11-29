import asyncio

import pyperclip
import typer

from utils.create_prompts import spr

app = typer.Typer(help="David's ShipIt Subcommands")


@app.command("spr")
def sparse_priming(
    paste_code: bool = typer.Option(
        True, "--paste", "-p", help="Paste code to update", is_flag=True
    ),
    max_tokens: int = typer.Option(250, "--max-tokens", "-m"),
):  # Changed function name
    if paste_code:
        typer.echo("Pasting code...")
        user_input = pyperclip.paste()
    else:
        user_input = typer.prompt("What would you like for me to generate?")

    asyncio.run(_sparse_priming(user_input, max_tokens))  # Changed function call


async def _sparse_priming(user_input, max_tokens):
    response = await spr(user_input, max_tokens)
    typer.echo(response)
    pyperclip.copy(response)
