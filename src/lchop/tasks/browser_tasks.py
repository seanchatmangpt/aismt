from loguru import logger

from lchop.context.task_context import register_task


@register_task
async def launch_browser(ctx, **kwargs):
    logger.info("Launching browser...")
    await ctx.browser_ctx.launch_browser(**kwargs)

    return {
        "success": True,
        "results": f"Successfully launched browser",
    }
