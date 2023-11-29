import os
from lchop.tasks.adsc_tasks import *

import typer
from importlib import import_module
from pathlib import Path

from typer import Context

from utils.complete import create
from utils.date_tools import next_friday
from shipit.shipit_project_config import (
    ShipitProjectConfig,
)  # Adjust the import path as necessary


from sqlmodel import SQLModel

app = typer.Typer()


def load_subcommands():
    script_dir = Path(__file__).parent
    subcommands_dir = script_dir / "subcommands"

    for filename in os.listdir(subcommands_dir):
        if filename.endswith("_cmd.py"):
            module_name = f"shipit.subcommands.{filename[:-3]}"
            module = import_module(module_name)
            if hasattr(module, "app"):
                app.add_typer(module.app, name=filename[:-7])


load_subcommands()

os.environ["TOKENIZERS_PARALLELISM"] = "(true | false)"


@app.callback()
def main(ctx: Context):
    from shipit.data import engine, get_session

    config_file = Path().cwd() / "shipit_project.yaml"
    SQLModel.metadata.create_all(engine)
    ctx.obj = {
        "config": ShipitProjectConfig.load(str(config_file)),
        "session": get_session(),
    }


@app.command()
def init(ctx: Context):
    """
    Initializes a new Shipit project and creates a configuration file.
    """
    # Prompt user for configuration details (can be expanded as needed)
    project_name = typer.prompt("Enter project name")
    description = typer.prompt("Enter project description")

    ship_date = typer.prompt(
        "Enter project due data in YYYY-MM-DD format", default=next_friday()
    )
    directory = typer.prompt("Enter directory for the project", default=str(Path.cwd()))

    # Create a new configuration object
    config = ShipitProjectConfig(
        project_name=project_name,
        description=description,
        ship_date=ship_date,
        directory=directory,
    )

    config.save()

    typer.echo(f"Initialized new Shipit project in {directory}")
    ctx.obj["config"] = config


if __name__ == "__main__":
    app()
