import subprocess
import anyio
import os
import importlib
from loguru import logger
from lchop.context.task_context import register_task
from lchop.context.work_context import default_work_context
from utils.create_prompts import create_python


@register_task
def ensure_dependency(dependency: str, use_poetry: bool = None):
    if use_poetry is None:
        use_poetry = os.path.isfile("pyproject.toml")
        logger.info(f"Poetry detected: {use_poetry}")

    try:
        importlib.import_module(dependency)
        logger.info(f"{dependency} is already installed.")
    except ImportError:
        logger.info(f"{dependency} is not installed. Installing now...")
        if use_poetry:
            subprocess.run(["poetry", "add", dependency], check=True)
            logger.info(f"{dependency} installed successfully using poetry.")
        else:
            subprocess.run(["pip", "install", dependency], check=True)
            logger.info(f"{dependency} installed successfully using pip.")


@register_task
async def create_virtual_environment(work_ctx, venv_name="my_venv", **kwargs):
    logger.info("Creating a new virtual environment.")
    ensure_dependency("virtualenv")
    subprocess.run(["virtualenv", venv_name], check=True)
    return {
        "success": True,
        "results": f"Successfully created virtual environment: {venv_name}.",
    }


@register_task
async def setup_poetry(work_ctx, **kwargs):
    ensure_dependency("poetry")
    logger.info("Poetry is set up for package management.")
    return {"success": True, "results": "Successfully set up Poetry."}


@register_task
async def add_flask_dependencies_with_poetry(work_ctx, **kwargs):
    dependencies = ["flask", "flask-sqlalchemy", "flask-migrate", "flask-login"]
    for dep in dependencies:
        ensure_dependency(dep, use_poetry=True)
    logger.info("Flask dependencies are set up using Poetry.")
    return {
        "success": True,
        "results": "Successfully added Flask dependencies using Poetry.",
    }


@register_task
async def start_flask_app(work_ctx, **kwargs):
    logger.info("Starting the Flask app with Poetry.")
    subprocess.run(["poetry", "run", "flask", "run"], check=True)
    return {
        "success": True,
        "results": "Successfully started the Flask app with Poetry.",
    }


@register_task
async def create_flask_app_from_ai(work_ctx, filename="app.py", **kwargs):
    """Creates a Flask app using the result from the AI model."""
    logger.info("Creating Flask App using the output from the AI model.")
    prompt = f"""
    Craft a 'Hello World' Flask application
    """
    await create_python(prompt=prompt, filepath=filename)

    return {
        "success": True,
        "results": f"Successfully created Flask app in {filename} using AI model output.",
    }


async def main():
    work_ctx = default_work_context()
    await create_virtual_environment(work_ctx)
    await setup_poetry(work_ctx)
    await create_flask_app_from_ai(work_ctx)
    await add_flask_dependencies_with_poetry(work_ctx)
    await start_flask_app(work_ctx)


if __name__ == "__main__":
    anyio.run(main)
