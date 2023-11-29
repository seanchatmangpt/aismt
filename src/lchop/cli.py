from click import group, command, option
from click.testing import CliRunner


@group()
def cli():
    """MetaCodeManufacturingPlant CLI"""
    pass


@cli.command()
@option("--project", default="None", help="Project name")
def init(project):
    """This is the init command"""
    print("Executing init with options:", project)


@cli.command()
@option("--workflow", default="None", help="Workflow file")
def validate(workflow):
    """This is the validate command"""
    print("Executing validate with options:", workflow)


@cli.command()
@option("--agent", default="None", help="Agent name")
@option("--task", default="None", help="Task name")
def build_backend(agent, task):
    """This is the build_backend command"""
    print("Executing build_backend with options:", agent, task)


@cli.command()
@option("--agent", default="None", help="Agent name")
@option("--task", default="None", help="Task summary")
def generate_dashboard(agent, task):
    """This is the generate_dashboard command"""
    print("Executing generate_dashboard with options:", agent, task)


@cli.command()
def test_backend():
    """This is the test_backend command"""
    print(
        "Executing test_backend with options:",
    )


def test_cli_commands():
    runner = CliRunner()

    print("Testing command: init")
    result = runner.invoke(cli, ["init"])
    print(result.output)

    print("Testing command: validate")
    result = runner.invoke(cli, ["validate"])
    print(result.output)

    print("Testing command: build_backend")
    result = runner.invoke(cli, ["build-backend"])
    print(result.output)

    print("Testing command: generate_dashboard")
    result = runner.invoke(cli, ["generate-dashboard"])
    print(result.output)

    print("Testing command: test_backend")
    result = runner.invoke(cli, ["test-backend"])
    print(result.output)


if __name__ == "__main__":
    cli()
