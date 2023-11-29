import pyperclip
import typer

from shipit.models import OptionConfig
from utils.file_tools import write


async def handle_output(
    config: OptionConfig
) -> None:
    output = config.output_file
    response = config.response
    auto_output = config.auto_save

    mode = "a+" if config.append_to_output else "w"

    if output:
        await write(response, filename=output, mode=mode)
    if auto_output:
        config.output_file = await write(response, extension=config.file_extension)

    pyperclip.copy(response)

    if config.verbose:
        typer.echo(f"Output: {response}")
        if output:
            typer.echo(f"Output saved to {output}")
        if auto_output:
            typer.echo(f"Output saved to {config.output_file}")
