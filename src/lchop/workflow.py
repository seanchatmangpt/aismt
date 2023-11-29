from lchop.context.work_context import *


def load_template_from_file(self, filename):
    try:
        with open(filename, "r") as f:
            template_str = f.read()
        self.env.from_string(template_str)
        logger.info(f"Successfully loaded template from file {filename}.")
    except Exception as e:
        logger.error(f"Failed to load template from file {filename}: {str(e)}")
        raise


def render_template_to_file(self, template_str, filename, **kwargs):
    try:
        rendered_content = self.render_template(template_str, **kwargs)
        with open(filename, "w") as f:
            f.write(rendered_content)
        logger.info(f"Successfully rendered template to file {filename}.")
    except Exception as e:
        logger.error(f"Failed to render template to file {filename}: {str(e)}")
        raise
