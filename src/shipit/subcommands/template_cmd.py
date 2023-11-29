import asyncio
from pathlib import Path

import typer

from shipit.models import OptionConfig
from typetemp.template.typed_template import TypedTemplate
from utils.complete import create
from utils.file_tools import get_project_root
from utils.output_tools import handle_output

app = typer.Typer()


class CommandDefTemplate(TypedTemplate):
    cmd_name: str
    source = """@app.command("{{ cmd_name }}")
def {{ cmd_name }}_command(
    prompt: str,
    model: str = typer.Option(
        "gpt-3.5-instruct",
        "-m",
        "--model",
        help="The OpenAI model to be used for AGI response.",
    ),
    input_file: str = typer.Option(None, "-i", "--input", help="Path to input file."),
    output_file: str = typer.Option(
        None, "-o", "--output", help="Path to output file."
    ),
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Enable verbose mode for printing output.", is_flag=True
    ),
    auto_save: bool = typer.Option(
        False,
        "-ao",
        "--auto-output",
        help="Automatically output to file with automatic file name.",
        is_flag=True,
    ),
    paste_from_clipboard: bool = typer.Option(
        False, "-p", "--paste", help="Paste input from the clipboard.", is_flag=True
    ),
    file_extension: str = typer.Option(
        None, "-ext", "--extension", help="File extension of auto output file."
    ),
    append_to_output: bool = typer.Option(
        False, "-a", "--append", help="Append to the output file.", is_flag=True
    ),
    max_tokens: int = typer.Option(
        250, "-mt", "--max-tokens", help="Max tokens to use for AGI response."
    ),
):
    config = OptionConfig(
        model=model,
        input_file=input_file,
        output_file=output_file,
        prompt=prompt,
        verbose=verbose,
        auto_save=auto_save,
        paste_from_clipboard=paste_from_clipboard,
        file_extension=file_extension,
        append_to_output=append_to_output,
        response=None,
        max_tokens=max_tokens
    )

    asyncio.run(_{{ cmd_name }}_command(config))

async def _{{ cmd_name }}_command(config: OptionConfig, **kwargs):
    if config.verbose:
        typer.echo(f"Running {{ cmd_name }} command... {config}")

    response = await acreate(prompt=config.prompt, max_tokens=config.max_tokens)

    if config.verbose:
        typer.echo(f"Response: {response}")

    config.response = response

    await handle_output(config)

    if config.verbose:
        typer.echo(f"{{ cmd_name }} command finished.")
    """


class CommandModuleTemplate(TypedTemplate):
    cmd_name: str
    command_def: CommandDefTemplate = CommandDefTemplate()
    source = """import asyncio

import typer

from shipit.models import OptionConfig
from utils.complete import acreate
from utils.output_tools import handle_output

app = typer.Typer()

{{ command_def }}


"""


@app.command("init")
def generate_command_from_template(
    module_name: str,
    command_name: str,
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Enable verbose mode for printing output.", is_flag=True
    ),
    auto_save: bool = typer.Option(
        False,
        "-ao",
        "--auto-output",
        help="Automatically output to file with automatic file name.",
        is_flag=True,
    ),
):
    # Create an instance of OptionConfig using the Typer options

    output_file = Path(get_project_root()) / f"src/shipit/subcommands/{module_name}_cmd.py"

    config = OptionConfig(
        output_file=str(output_file),
        verbose=verbose,
        auto_save=auto_save,
        response=CommandModuleTemplate(cmd_name=command_name)()
    )

    if config.verbose:
        typer.echo(f"Running init command... {config}")

    asyncio.run(handle_output(config))


@app.command("cmd")
def add_command_from_template(
    module_name: str,
    command_name: str,
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Enable verbose mode for printing output.", is_flag=True
    ),
    auto_save: bool = typer.Option(
        False,
        "-ao",
        "--auto-output",
        help="Automatically output to file with automatic file name.",
        is_flag=True,
    ),
):
    # Create an instance of OptionConfig using the Typer options

    output_file = Path(get_project_root()) / f"src/shipit/subcommands/{module_name}_cmd.py"

    config = OptionConfig(
        output_file=str(output_file),
        verbose=verbose,
        auto_save=auto_save,
        response=CommandDefTemplate(cmd_name=command_name)(),
        append_to_output=True
    )

    if config.verbose:
        typer.echo(f"Running init command... {config}")

    asyncio.run(handle_output(config))


if __name__ == "__main__":
    print(CommandModuleTemplate(cmd_name="test")())
