import asyncio
import json
import time
from dataclasses import dataclass


from loguru import logger

from lchop.context.task_context import register_task
from typetemp.template.typed_template import TypedTemplate
from utils.complete import acreate
from utils.models import best_models


@dataclass
class SarahMikeEmailTemplate(TypedTemplate):
    name: str = None
    location: str = None
    date: str = None
    topic: str = None
    sender_name: str = None
    source = """
Dear {{ name }},

I hope this message finds you well in {{ location }}. 
I wanted to remind you about our appointment on {{ date }} 
regarding {{ topic }}. Please let me know if you need to reschedule.

Best regards,
{{ sender_name }}
    """


email_prompt = """
Objective:
Generate a Python dictionary to populate the given Jinja template, based on the information from the provided paragraph.


Dear {{ name }},

I hope this message finds you well in {{ location }}. 
I wanted to remind you about our appointment on {{ date }} 
regarding {{ topic }}. Please let me know if you need to reschedule.

Best regards,
{{ sender_name }}

Paragraph:
Sarah lives in New York and recently mentioned she would like to discuss the new project proposal. Our meeting is set for June 12th, and if she's unavailable, she should contact Mike.

Chain of Thought:
Extract the name of the person the letter is addressed to.
Identify the location where the person lives.
Find the date of the meeting/appointment.
Determine the topic of the discussion/meeting.
Identify who the sender or the point of contact is.
Additional Information:
The name is the person being addressed in the paragraph.
location is the place where the named person resides.
The date represents the scheduled day for the event or meeting.
topic signifies what the meeting or event is about.
sender_name is the individual to be contacted in case of any changes.
Please produce the perfect Python dictionary based on the given data.
"""


@register_task
async def Setup_Environment(work_ctx, models, prompt, template_class, **kwargs):
    logger.info(f"Executing task: Setup_Environment")
    work_ctx.global_kwargs.start = time.time()

    work_ctx.global_kwargs.models = models
    work_ctx.global_kwargs.prompt = prompt
    work_ctx.global_kwargs.template_class = template_class

    return {"success": True, "results": f"Successfully executed: Setup_Environment"}


@register_task
async def Run_GPT_Models(work_ctx, **kwargs):
    logger.info(f"Executing task: Run_GPT_Models")

    async def run_model(model):
        result = await acreate(
            model=model,
            prompt=email_prompt,
            temperature=0.0,
            max_tokens=100,
            stop=["}"],
        )
        if "sender_name" in result:
            return model, result
        else:
            return None, None

    tasks = [run_model(model) for model in best_models * 20]
    results = await asyncio.gather(*tasks)

    work_ctx.raw_results = results

    return {"success": True, "results": f"Successfully executed: Run_GPT_Models"}


@register_task
async def Filter_Valid_Results(work_ctx, **kwargs):
    logger.info(f"Executing task: Filter_Valid_Results")

    valid_results = [
        (model, result) for model, result in work_ctx.raw_results if model and result
    ]
    work_ctx.valid_results = valid_results

    return {"success": True, "results": f"Successfully executed: Filter_Valid_Results"}


@register_task
async def Generate_Emails(work_ctx, **kwargs):
    logger.info(f"Executing task: Generate_Emails")

    generated_emails = []

    for model, result in work_ctx.valid_results:
        kwargs = json.loads(result + "}")
        email = SarahMikeEmailTemplate(**kwargs)()
        generated_emails.append(email)

    work_ctx.generated_emails = generated_emails

    return {"success": True, "results": f"Successfully executed: Generate_Emails"}


@register_task
async def Save_To_Files(work_ctx, **kwargs):
    logger.info(f"Executing task: Save_To_Files")

    for idx, email in enumerate(work_ctx.generated_emails):
        to = f"./emails/email_{idx}_{time.time()}.txt"
        with open(to, "w") as f:
            f.write(email)

    return {"success": True, "results": f"Successfully executed: Save_To_Files"}


@register_task
async def Display_Results_Summary(work_ctx, start_time, **kwargs):
    logger.info(f"Executing task: Display_Results_Summary")

    end = time.time()
    duration = end - work_ctx.global_kwargs.start
    valid_model_count = len(work_ctx.valid_results)

    return {
        "success": True,
        "results": f"Duration: {duration}. Total models: {valid_model_count}",
    }
