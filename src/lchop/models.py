from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from lchop.context.work_context import default_work_context, load_workflow
from lchop.tasks.template_tasks import generate_task_code_from_workflow
from utils.yaml_tools import YAMLMixin


class Task(BaseModel, YAMLMixin):
    name: str
    description: str
    kwargs: Dict[str, Any]


class Workflow(BaseModel, YAMLMixin):
    global_kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict)
    tasks: List[Task] = Field(default_factory=list)


workflow = Workflow(
    global_kwargs={},
    tasks=[
        Task(
            name="review_generative_ai_page",
            description="Review the page on Generative AI on ADSC's website.",
            kwargs={
                "website_url": "https://www.adscke.com/index.php/adsc-sales-marketing-generative-ai-services/"
            },
        ),
        Task(
            name="generate_power_of_generative_ai_subpage",
            description="Generate a sub-page explaining the power of Generative AI.",
            kwargs={
                "topic": "Power of Generative AI",
                "prompt": "Please generate a detailed sub-page explaining the power of Generative AI and its applications.",
            },
        ),
        Task(
            name="generate_custom_generative_ai_agents_subpage",
            description="Generate a sub-page explaining how ADSC can help create custom Generative AI Agents.",
            kwargs={
                "topic": "Custom Generative AI Agents",
                "prompt": "Please create a sub-page highlighting how ADSC's expertise can assist in the creation of custom Generative AI Agents.",
            },
        ),
        Task(
            name="generate_use_of_synthetic_data_subpage",
            description="Generate a sub-page explaining the use of synthetic data and its importance.",
            kwargs={
                "topic": "Use of Synthetic Data",
                "prompt": "Create a sub-page elaborating on the significance of synthetic data and its role in AI development.",
            },
        ),
        Task(
            name="generate_privacy_compliance_subpage",
            description="Generate a sub-page explaining privacy compliance in the context of Generative AI.",
            kwargs={
                "topic": "Privacy Compliance",
                "prompt": "Please generate a sub-page discussing privacy compliance considerations when using Generative AI.",
            },
        ),
        Task(
            name="generate_internal_custom_agents_subpage",
            description="Generate a sub-page explaining how internal custom agents can support sales and marketing.",
            kwargs={
                "topic": "Internal Custom Agents",
                "prompt": "Create a sub-page highlighting how internal custom agents can enhance sales and marketing processes.",
            },
        ),
        Task(
            name="generate_saas_sales_subpage",
            description="Generate a sub-page explaining the potential for SAAS sales of subscriptions with insights wrapped as custom agents.",
            kwargs={
                "topic": "SAAS Sales of Subscriptions",
                "prompt": "Please create a sub-page discussing the potential for SAAS sales of subscriptions with insights as custom agents.",
            },
        ),
        Task(
            name="generate_synthetic_data_subpage",
            description="Generate a sub-page explaining the concept of synthetic data.",
            kwargs={
                "topic": "Synthetic Data",
                "prompt": "Generate a sub-page explaining the concept of synthetic data and its applications in AI development.",
            },
        ),
        Task(
            name="apply_styling_for_wordpress_and_adsc_website",
            description="Apply appropriate styling to fit WordPress and the current ADSC website.",
            kwargs={"styling_type": "WordPress and ADSC Website"},
        ),
        Task(
            name="generate_html_for_implementation",
            description="Generate HTML code for implementation on the ADSC website.",
            kwargs={"output_format": "HTML"},
        ),
    ],
)

# workflow = Workflow(tasks=workflow_data)
# print(workflow)

workflow.to_yaml("workflow.yaml")

import anyio


async def main():
    # adsc = Workflow.from_yaml("workflow.yaml")
    # print(adsc)
    await generate_task_code_from_workflow(
        work_ctx=default_work_context(),
        workflow_path="workflow.yaml",
        task_code_path="sub_page_tasks.py",
    )
    # await load_workflow("workflow.yaml")


if __name__ == "__main__":
    anyio.run(main)
