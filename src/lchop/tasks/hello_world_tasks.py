from loguru import logger

from lchop.context.task_context import register_task


@register_task
async def print_hello(work_ctx, message="Hello, World!", full_name="", **kwargs):
    logger.info(f"Executing task: print_hello")
    logger.info(f"Message: {message} {full_name}")
    return {"success": True, "results": f"Successfully printed: {message} {full_name}"}


@register_task
async def print_goodbye(work_ctx, message="Goodbye, World!", full_name="", **kwargs):
    logger.info(f"Executing task: print_goodbye")
    logger.info(f"Message: {message} {full_name}")
    return {"success": True, "results": f"Successfully printed: {message} {full_name}"}
