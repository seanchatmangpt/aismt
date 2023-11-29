import importlib
import os

from loguru import logger

# print(f"Importing tasks...")
#
# # Get the current directory (where __init__.py is located)
# current_directory = os.path.dirname(__file__)
#
# # List all files in the current directory
# all_files = os.listdir(current_directory)
#
# # Filter the files to get only Python module files (ending with .py)
# module_files = [
#     file[:-3] for file in all_files if file.endswith(".py") and file != "__init__.py"
# ]
#
# # Dynamically import all modules
# for module_name in module_files:
#     module = importlib.import_module(f".{module_name}", package=__name__)
#     logger.info(f"Imported module: {module_name}")

# from .gen_email_tasks import *
