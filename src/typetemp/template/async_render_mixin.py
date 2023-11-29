import aiofiles
import os
from typing import Any, Dict

import anyio

from typetemp.environment.typed_environment import async_environment
from typetemp.environment.typed_native_environment import async_native_environment
from typetemp.template.render_funcs import arender_str
from utils.complete import acreate


class AsyncRenderMixin:
    """
    An async mixin class that encapsulates the render and _render_vars functionality.
    """

    async def _render(self, use_native=False, **kwargs) -> Any:
        """
        Render the template.
        """
        self._env = async_native_environment if use_native else async_environment

        template = self._env.from_string(
            self.source
        )  # Assuming self.env is a jinja2.Environment

        render_dict = kwargs.copy()
        render_dict.update(await self._render_vars())

        self.output = await template.render_async(**render_dict)

        await self._llm_call()

        if self.to == "stdout":
            print(self.output)
        elif self.to:
            # to_template = self._env.from_string(self.to)
            rendered_to = (
                self.to
            )  # os.path.join(await to_template.render(**render_dict))  # If needed, make this async too

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(rendered_to), exist_ok=True)
            rendered_to = os.path.abspath(rendered_to)

            async with aiofiles.open(
                rendered_to, "w"
            ) as file:  # Using aiofiles for async file operations
                await file.write(self.output)

        return self.output

    async def _render_vars(self) -> Dict[str, Any]:
        properties = self.__dict__.copy()
        properties.update(self.__class__.__dict__)

        async with anyio.create_task_group() as tg:
            for name, value in properties.items():
                if isinstance(value, AsyncRenderMixin):
                    tg.start_soon(self._concurrent_render, name, value, properties)
                elif isinstance(value, str):
                    properties[name] = await arender_str(value)

        return properties

    async def _concurrent_render(
        self, name: str, value: "AsyncRenderMixin", properties: Dict[str, Any]
    ):
        properties[name] = await value._render()

    async def _llm_call(self):
        """
        Use a LLM to render the template as a prompt.
        """
        if self.config:
            self.output = await acreate(prompt=self.output, config=self.config)
