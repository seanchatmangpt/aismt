import asyncio
from pathlib import Path

import anyio
import pyperclip
import typer
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from typer import Context

from utils.complete import create
from utils.create_prompts import create_python
from utils.radon_workbench import fix_code

app = typer.Typer(help="Advanced Coding Assistant")


@app.command()
def module(
    ctx: Context,
    filename: str = typer.Argument(..., help="The name of the module to generate"),
):
    """Generate module"""
    typer.echo("Generating module prompt...")
    prompt = typer.prompt("Enter a prompt for the module")
    asyncio.run(create_python(prompt=prompt, filepath=f"{Path.cwd()}/{filename}"))
    typer.echo("Module generated successfully.")


@app.command("fix")
def fix_clipboard():
    """Take the code in the clipboard, fix it with OpenAI, and replace contents of clipboard with fixed code."""
    code = pyperclip.paste()

    fixed = fix_code(code=code)

    pyperclip.copy(fixed)

    typer.echo(fixed)

    typer.echo("Code fixed successfully.")


# Utility Functions
def generate_context(task_description, max_tokens=2000):
    """
    Generate context based on the task description.
    """
    try:
        prompt = f"Create a context with examples, labels, and instructions for the task: {task_description}"
        return create(prompt=prompt, max_tokens=max_tokens)
    except Exception as e:
        return f"Error generating context: {e}"


def solve_task_with_context(task_description, context, max_tokens=2000):
    """
    Solve a task using the generated context.
    """
    try:
        prompt = f"Given the context: {context}\nSolve the task: {task_description}"
        return create(prompt=prompt, max_tokens=max_tokens)
    except Exception as e:
        return f"Error solving task: {e}"


# Command: AI Integration
def ai_integration_context(model, target):
    task_description = (
        f"Task: Integrate the AI model '{model}' into the software component '{target}'. "
        f"Deliver a step-by-step guide on how to embed the model, ensure seamless data flow, "
        f"and maintain optimal performance. Include code snippets for critical integration points."
    )
    return generate_context(task_description)


# Command: System Optimization
def sys_optimization_context(system, focus):
    task_description = (
        f"Task: Conduct a performance optimization of the system '{system}' with a focus on '{focus}'. "
        f"Deliver a detailed analysis of current bottlenecks, followed by a comprehensive optimization plan. "
        f"Include specific code refactorings and architectural changes that can enhance system efficiency."
    )
    return generate_context(task_description)


# Command: Code Generation
def code_generation_context(language, feature):
    task_description = (
        f"Task: Generate a functional code module in '{language}' for the feature '{feature}'. "
        f"Deliver a complete module that adheres to best practices in coding and design patterns. "
        f"Ensure the code is well-commented, scalable, and includes unit tests for all major functions."
    )
    return generate_context(task_description)


# Command: AI Integration
@app.command("ai")
def ai_integrate(
    model: str = typer.Option(..., help="AI model name"),
    target: str = typer.Option(..., help="Target software component for integration"),
    max_tokens: int = typer.Option(
        200, help="Maximum number of tokens for OpenAI API response"
    ),
):
    """
    Integrate an AI model into a software component.
    """
    context = generate_context(
        f"Integrate AI model '{model}' into '{target}'", max_tokens
    )
    solution = solve_task_with_context(
        f"Integrate AI model '{model}' into '{target}'", context, max_tokens
    )
    typer.echo("Solution:\n" + solution)


# Command: System Optimization
@app.command("sys")
def sys_optimize(
    system: str = typer.Option(..., help="System to be optimized"),
    focus: str = typer.Option(..., help="Focus area of optimization"),
    max_tokens: int = typer.Option(
        200, help="Maximum number of tokens for OpenAI API response"
    ),
):
    """
    Optimize the performance of a specific system.
    """
    context = generate_context(
        f"Optimize system '{system}' focusing on '{focus}'", max_tokens
    )
    solution = solve_task_with_context(
        f"Optimize system '{system}' focusing on '{focus}'", context, max_tokens
    )
    typer.echo("Solution:\n" + solution)


# Command: Code Generation
@app.command("gen")
def code_gen(
    language: str = typer.Option(..., help="Programming language for code generation"),
    feature: str = typer.Option(..., help="Feature to be implemented in code"),
    max_tokens: int = typer.Option(
        200, help="Maximum number of tokens for OpenAI API response"
    ),
):
    """
    Generate code for a specified feature in a given programming language.
    """
    context = generate_context(
        f"Generate code in '{language}' for feature '{feature}'", max_tokens
    )
    solution = solve_task_with_context(
        f"Generate code in '{language}' for feature '{feature}'", context, max_tokens
    )
    typer.echo("Solution:\n" + solution)


@app.command()
def query():
    python_completer = WordCompleter(["print", "def", "class", "import", "from"])
    user_input = prompt(">>> ", completer=python_completer)
    typer.echo(f"You entered: {user_input}")


@app.command("nextgen")
def code_gen(
    language: str = typer.Option(..., help="Programming language for code generation"),
    feature: str = typer.Option(..., help="Feature to be implemented in code"),
    max_tokens: int = typer.Option(
        200, help="Maximum number of tokens for OpenAI API response"
    ),
):
    """
    Generate code for a specified feature in a given programming language.
    Allows iterative refinement based on user feedback.
    """
    global solution
    satisfied = False
    context = generate_context(
        f"Generate code in '{language}' for feature '{feature}'", max_tokens
    )

    while not satisfied:
        solution = solve_task_with_context(
            f"Generate code in '{language}' for feature '{feature}'",
            context,
            max_tokens,
        )
        typer.echo("Generated Code:\n" + solution)

        # Ask for user feedback
        feedback = typer.prompt(
            "Review the code. If you need changes, describe them; otherwise type 'done'"
        )
        if feedback.lower() == "done":
            satisfied = True
        else:
            # Modify the context with user feedback for further refinement
            context = modify_context_with_feedback(context, feedback, language, feature)

    typer.echo("Final Code:\n" + solution)


def modify_context_with_feedback(
    context: str, feedback: str, language: str, feature: str
) -> str:
    """
    Modify the context by incorporating user feedback.
    """
    updated_context = f"{context}\n\nFeedback: {feedback}\n\nModify the '{language}' code for '{feature}' accordingly."
    return updated_context


import asyncio
from textwrap import dedent

import typer
import pyperclip

from utils.create_prompts import create_code  # Changed from create_python


@app.command("bot")
def update_code_code(
    paste_code: bool = typer.Option(
        False, "--paste", "-p", help="Paste code to update"
    ),
    language: str = typer.Option("code", "--language", "-l"),
):  # Changed function name
    if paste_code:
        print(pyperclip.paste())
        user_input = typer.prompt("How would you like this code updated?")
        user_input = pyperclip.paste() + "\n\nUser: I would like to have " + user_input
    else:
        user_input = typer.prompt("What would you like for me to generate?")

    asyncio.run(_update_code_code(user_input, language))  # Changed function call


async def _update_code_code(user_input, language):  # Changed function name
    print("Generating code snippet...", user_input, language)
    code = user_input

    code = await create_code(
        prompt=code, language=language
    )  # Changed from create_python

    # Display code snippet details and ask for confirmation
    confirmed = False
    while not confirmed:
        print(f"Code Snippet Details:\n{code}")

        confirm = typer.prompt("Are these details correct? [y/N]")
        if confirm.lower() in ["y", "yes"]:
            confirmed = True
        else:
            # Re-prompt for details
            update_prompt = f"{code}\nUser: {confirm}"
            code = await create_code(
                prompt=update_prompt, language=language
            )  # Changed from create_python

    pyperclip.copy(code)
    print(f"Code copied to clipboard.")


if __name__ == "__main__":
    app()
