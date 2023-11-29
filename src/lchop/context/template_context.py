import os

from loguru import logger
from munch import Munch

from typetemp.environment.typed_environment import TypedEnvironment


class TemplateContext:
    def __init__(self):
        try:
            self.env = TypedEnvironment()
            self.templates = Munch()
            logger.info(f"TemplateContext initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize the Jinja environment: {str(e)}")
            raise

    def render_file_template(self, file_path, **kwargs):
        try:
            if not os.path.exists(file_path):
                raise Exception(f"File {file_path} does not exist.")

            with open(file_path, "r") as f:
                template_str = f.read()

            return self.render_template(template_str, **kwargs)
        except Exception as e:
            logger.error(f"Failed to load template from file: {str(e)}")
            raise

    def render_template(self, template_str, **kwargs):
        try:
            template = self.env.from_string(template_str)

            return template.render(**kwargs)
        except Exception as e:
            logger.error(f"Failed to render template: {str(e)}")
            raise

    def set_variable(self, name, value):
        try:
            self.env.globals[name] = value
            logger.info(f"Set global variable {name}.")
        except Exception as e:
            logger.error(f"Failed to set variable {name}: {str(e)}")
            raise

    def get_variable(self, name):
        try:
            value = self.env.globals.get(name, None)
            logger.info(f"Fetched global variable {name}.")
            return value
        except Exception as e:
            logger.error(f"Failed to get variable {name}: {str(e)}")
            raise
