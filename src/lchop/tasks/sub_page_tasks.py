from loguru import logger
from lchop.context.task_context import register_task
from utils.create_prompts import create_tailwind_landing


@register_task
async def review_generative_ai_page(work_ctx, website_url, **kwargs):
    logger.info(f"Executing task: review_generative_ai_page")

    # Task-specific code here...

    return {
        "success": True,
        "results": f"Successfully executed: review_generative_ai_page",
    }


@register_task
async def generate_power_of_generative_ai_subpage(work_ctx, prompt, topic, **kwargs):
    logger.info(f"Executing task: generate_power_of_generative_ai_subpage")

    await create_tailwind_landing(
        prompt=prompt, title=topic, filepath="power_of_generative_ai.html"
    )

    return {
        "success": True,
        "results": f"Successfully executed: generate_power_of_generative_ai_subpage",
    }


@register_task
async def generate_custom_generative_ai_agents_subpage(
    work_ctx, prompt, topic, **kwargs
):
    logger.info(f"Executing task: generate_custom_generative_ai_agents_subpage")

    await create_tailwind_landing(
        prompt=prompt, title=topic, filepath="custom_generative_ai_agents.html"
    )

    return {
        "success": True,
        "results": f"Successfully executed: generate_custom_generative_ai_agents_subpage",
    }


@register_task
async def generate_use_of_synthetic_data_subpage(work_ctx, prompt, topic, **kwargs):
    logger.info(f"Executing task: generate_use_of_synthetic_data_subpage")

    await create_tailwind_landing(
        prompt=prompt, title=topic, filepath="use_of_synthetic_data.html"
    )

    return {
        "success": True,
        "results": f"Successfully executed: generate_use_of_synthetic_data_subpage",
    }


@register_task
async def generate_privacy_compliance_subpage(work_ctx, prompt, topic, **kwargs):
    logger.info(f"Executing task: generate_privacy_compliance_subpage")

    await create_tailwind_landing(
        prompt=prompt, title=topic, filepath="privacy_compliance.html"
    )

    return {
        "success": True,
        "results": f"Successfully executed: generate_privacy_compliance_subpage",
    }


@register_task
async def generate_internal_custom_agents_subpage(work_ctx, prompt, topic, **kwargs):
    logger.info(f"Executing task: generate_internal_custom_agents_subpage")

    await create_tailwind_landing(
        prompt=prompt, title=topic, filepath="internal_custom_agents.html"
    )

    return {
        "success": True,
        "results": f"Successfully executed: generate_internal_custom_agents_subpage",
    }


@register_task
async def generate_saas_sales_subpage(work_ctx, prompt, topic, **kwargs):
    logger.info(f"Executing task: generate_saas_sales_subpage")

    await create_tailwind_landing(
        prompt=prompt, title=topic, filepath="saas_sales.html"
    )

    return {
        "success": True,
        "results": f"Successfully executed: generate_saas_sales_subpage",
    }


@register_task
async def generate_synthetic_data_subpage(work_ctx, prompt, topic, **kwargs):
    logger.info(f"Executing task: generate_synthetic_data_subpage")

    await create_tailwind_landing(
        prompt=prompt, title=topic, filepath="synthetic_data.html"
    )

    return {
        "success": True,
        "results": f"Successfully executed: generate_synthetic_data_subpage",
    }
