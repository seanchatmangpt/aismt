from typing import Any

from ..environment.typed_environment import environment, async_environment
from ..environment.typed_native_environment import (
    native_environment,
    async_native_environment,
)


def render_str(source, **kwargs) -> str:
    template = environment.from_string(source)

    return template.render(**kwargs)


async def arender_str(source, **kwargs) -> str:
    template = async_environment.from_string(source)

    return await template.render_async(**kwargs)


def render_py(source, env=native_environment, **kwargs) -> Any:
    template = env.from_string(source)

    return template.render(**kwargs)


async def arender_py(source, env=async_native_environment, **kwargs) -> Any:
    template = env.from_string(source)

    return await template.render_async(**kwargs)
