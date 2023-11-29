import asyncio

import typer
import os

from utils.complete import create
from utils.file_tools import read, write
from utils.gherkin_parser import GherkinParser

app = typer.Typer(help="Behavior-driven development (BDD) utilities.")


@app.command("parse")
def generate_pytest_code(
    input_file: str = typer.Option(
        ..., "-i", "--input", help="Input Gherkin feature file path"
    ),
    output_file: str = typer.Option(
        None, "-o", "--output", help="Output Pytest code file path"
    ),
):
    """
    Read the Gherkin feature from the input file and parse it.
    """
    asyncio.run(_generate_pytest_code(input_file, output_file))


async def _generate_pytest_code(input_file: str, output_file: str | None = None):
    """
    Read the Gherkin feature from the input file and parse it.
    """
    gherkin_text = await read(input_file)
    # Create a GherkinParser and generate Pytest code
    parser = GherkinParser(gherkin_text)
    pytest_code = parser.generate_pytest_code()

    output_file = await write(pytest_code, filename=output_file, extension="py")
    typer.echo(f"Pytest code written to {output_file}")


# Create gherkin feature file from prompt


@app.command("create")
def create_gherkin_feature(
    prompt: str = typer.Option(
        ..., "-p", "--prompt", help="Prompt for Gherkin feature"
    ),
):
    """
    Create a Gherkin feature file from a prompt.
    """
    gpt_prompt = f"""You are a Gherkin assistant that creates a Gherkin feature file
    from a prompt:
    
    ```prompt
    {prompt}
    ```
    
    ```gherkin"""

    typer.echo(
        create(prompt=gpt_prompt, max_tokens=1000, temperature=0.9, stop=["```"])
    )


if __name__ == "__main__":
    app()
