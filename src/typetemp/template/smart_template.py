from textwrap import dedent

from typetemp.template.async_render_mixin import AsyncRenderMixin
from utils.complete import LLMConfig


class SmartTemplate(AsyncRenderMixin):
    """
    Base class for creating templated classes. Uses the jinja2 templating engine
    to render templates. Allows for usage of macros and filters.
    """

    config: LLMConfig = None  # The LLMConfig object
    source: str = None  # The string template to be rendered
    to: str = None  # The "to" property for rendering destination
    output: str = None  # The rendered output

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.config = LLMConfig() if "config" not in kwargs else kwargs["config"]

    async def render(self, use_native=False, **kwargs) -> str:
        # Use NativeEnvironment when use_native is True, else use default Environment
        self.source = dedent(self.source)
        await self._render(use_native=use_native, **kwargs)

        return self.output


import anyio


async def main():
    # Initialize LLMConfig and create 50 sub-templates
    config = LLMConfig(max_tokens=10)
    sub_templates = {
        f"sub_template_{i}": SmartTemplate(source=f"Sub template {i}") for i in range(1)
    }

    # Initialize SmartTemplate with 50 sub-templates
    template = SmartTemplate(config=config, source="Main template", **sub_templates)

    # Render the main template
    print(await template.render())

    # Optionally print outputs of sub-templates
    for i in range(1):
        print(
            f"Sub Template {i} Output:", getattr(template, f"sub_template_{i}").output
        )


if __name__ == "__main__":
    anyio.run(main)
