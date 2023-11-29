import asyncio
from dataclasses import dataclass

from lchop.context.task_context import register_task
from typetemp.template.typed_prompt import TypedPrompt


@dataclass
class NewTypedPrompt(TypedPrompt):
    message: str = None
    source = "Hello, {{ message }}"


@register_task
async def type_prompt(work_ctx, message="Hello, World!", **kwargs):
    temp = NewTypedPrompt(message=message)
    return {"success": True, "results": f"Successfully templated: {temp()}"}


# if __name__ == "__main__":
# work_ctx = default_work_context()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(type_prompt(work_ctx))
# print(work_ctx.task_ctx.results)
