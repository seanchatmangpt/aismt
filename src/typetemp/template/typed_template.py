from typetemp.template.render_mixin import RenderMixin


class TypedTemplate(RenderMixin):
    """
    Base class for creating templated classes. Uses the jinja2 templating engine
    to render templates. Allows for usage of macros and filters.
    """

    source: str = None  # The string template to be rendered
    to: str = None  # The "to" property for rendering destination
    output: str = None  # The rendered output

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, use_native=False, **kwargs) -> str:
        # Use NativeEnvironment when use_native is True, else use default Environment
        return self._render(use_native, **kwargs)
