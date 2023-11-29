from loguru import logger
from lchop.context.task_context import register_task

import json
import time
from itertools import islice

from duckduckgo_search import DDGS

from utils.create_prompts import create_tailwind_landing
from utils.prompt_tools import batched_prompt_map

DUCKDUCKGO_MAX_ATTEMPTS = 3

import asyncio
import aiohttp

import asyncio
import aiohttp
import bs4


async def extract_text(url):
    # create a session
    async with aiohttp.ClientSession() as session:
        # get response from url
        response = await session.get(url)
        # read response as text
        text = await response.text()
        # return BeautifulSoup object
        return bs4.BeautifulSoup(text, "html.parser")


async def download_and_extract(urls):
    # create a session
    async with aiohttp.ClientSession() as session:
        # create a list of tasks
        tasks = [asyncio.create_task(extract_text(url)) for url in urls]
        # wait for all tasks to be completed
        results = await asyncio.gather(*tasks)
        # return list of extracted texts
        return [result.get_text() for result in results]


import re


def extract_hyperlinks(input_string):
    """
    Extracts hyperlinks from a string and returns them in a list.
    Args:
        input_string(str): String to extract hyperlinks from.
    Returns:
        List(str): List of hyperlinks found in the string.
    """
    return re.findall(r"(https?://\S+)", input_string)


async def web_search(query: str, num_results: int = 5) -> list[str]:
    """Return the results of a Google search

    Args:
        query (str): The search query.
        num_results (int): The number of results to return.

    Returns:
        str: The results of the search.
    """
    search_results = []
    attempts = 0

    while attempts < DUCKDUCKGO_MAX_ATTEMPTS:
        results = DDGS().text(query)
        search_results = list(islice(results, num_results))

        if search_results:
            break

        time.sleep(1)
        attempts += 1

    results = json.dumps(search_results, ensure_ascii=False, indent=4)
    return json.loads(safe_google_results(results))


def safe_google_results(results: str | list) -> str:
    """
        Return the results of a Google search in a safe format.

    Args:
        results (str | list): The search results.

    Returns:
        str: The results of the search.
    """
    if isinstance(results, list):
        safe_message = json.dumps(
            [result.encode("utf-8", "ignore").decode("utf-8") for result in results]
        )
    else:
        safe_message = results.encode("utf-8", "ignore").decode("utf-8")
    return safe_message


@register_task
async def competitive_analysis_ADSC(work_ctx, services, revenue_threshold, **kwargs):
    logger.info(f"Executing task: competitive_analysis_ADSC")

    prompt = """Please do a competitive analysis of Applied Direct Services Corporation, Also Known As ADSC, whose website is located at https://www.applieddirectservicescorp.com/ and also at https://www.adscke.com/index.php/adsc-ethical-competitive-intelligence-services/ and also at https://www.adscke.com/index.php/adsc-sales-marketing-generative-ai-services/ an act as an expert on Enterprise Sales and Marketing, Competitive Intelligence and Generative AI. Please do a comparative analysis via SWOT of this group versus their top 5 competitors only for Competitive Intelligence Services and Generative AI Services and no other services, and please avoid large companies as they are in a different category, the competitors should have no more than $50 Million of gross annual revenue, and after that do a comparative VRIO analysis of these groups as well. Gather this information for further steps of Dataflow. Only look at two core service offerings that ADSC offers as follows and nothing else:
Ethical Competitive Intelligence Services.
Generative AI Services
And do not look at anything else that ADSC does. Learn about them.
"""

    # links = extract_hyperlinks(prompt)

    # adsc_texts = await download_and_extract(links)

    competitors = await web_search(
        "List of Ethical Competitive Intelligence Services", num_results=25
    )

    companies = await batched_prompt_map(
        prompts_iterable=competitors,
        base_prompt="Tell me the name of the "
        "Intelligence Service Company or None:\n",
    )

    return {
        "success": True,
        "results": f"Successfully executed: competitive_analysis_ADSC",
        "companies": companies,
    }


import anyio


@register_task
async def analyze_competitors(work_ctx, number_of_competitors, **kwargs):
    logger.info(f"Executing task: analyze_competitors")

    prompt = """ADSC can be a valuable partner to your Ethical Competitive Intelligence efforts.

We can support your creation of an Ethical Competitive Intelligence program from scratch.

Throughout your Ethical Competitive Intelligence processes, we can both train and/or support your team to better enable:

Data Acquisition.
Secure Online Recording of Such Information.
Analysis Of Information.
Assembling Of The Big Picture Meaning Of Such Information
Attribution
We can train your team to better deal with these five business processes. Alternatively, we can also organize your team on how to orchestrate these kinds of business processes.

In this way we can help you & your team to better know on an ongoing basis, the factors relevant to your business involving:

Customers
Prospects
Competitors
External Forces.
Therefore, we can provide a means for you to either ethically enhance your existing Competitive Intelligence Program or to start such a program from scratch.

Please contact us as shown below:

Applied Direct Services Corporation (ADSC) 
Please do a competitive analysis of the top 5 competitors from the last prompt and do both a 
    comparative chart with SWOT and then VRIO between ADSC and it’s competitors. Please show this and then show a 
    chart showing the positioning against Maslow’s Hierarchy of human needs for these competitors versus ADSC."""

    await create_tailwind_landing(prompt=prompt, filepath="analyze_competitors.html")
    return {"success": True, "results": f"Successfully executed: analyze_competitors"}


@register_task
async def create_landing_page_CI_AI_services(
    work_ctx, emphasize_CI, target_audience, call_to_action, **kwargs
):
    logger.info(f"Executing task: create_landing_page_CI_AI_services")

    landing_prompt = f"""
    ADSC relaunching two services: Ethical Competitive Intelligence Services and Generative AI Services. Keep track of Competitors, Customers, Prospects, Vendors, and external forces. CI is about positioning and predicting better next moves than anyone else. ADSC uses Generative AI for CI, Sales & Marketing agents, and can create other custom Generative AI based Agents. Landing Page: summary, contact info, catchy for professional audience. Call to action: free half-hour consultation to supercharge sales and marketing processes. Landing Page with different forms based on questions. First question: have they ever been blind-sided by a competitor or lost out unexpectedly? HTML generated for Landing Page/Form.
    """

    await create_tailwind_landing(
        prompt=landing_prompt,
        filepath="/Users/candacechatman/dev/shipit/build/ci_ai_services.html",
    )

    return {
        "success": True,
        "results": f"Successfully executed: create_landing_page_CI_AI_services",
    }


@register_task
async def generate_follow_up_forms(
    work_ctx, question_types, response_based_branching, **kwargs
):
    logger.info(f"Executing task: generate_follow_up_forms")

    landing_prompt = f"""
    This is a process that collects information from users through a series of questions and then provides them with a 
    competitive analysis of their top five competitors. The analysis is presented in chart form and users are asked 
    to provide their knowledge about each competitor. Users are also given the option to request a free half hour 
    consultation. 
    """

    await create_tailwind_landing(
        prompt=landing_prompt,
        filepath="/Users/candacechatman/dev/shipit/build/follow_up_forms.html",
    )

    return {
        "success": True,
        "results": f"Successfully executed: generate_follow_up_forms",
    }


@register_task
async def create_synthetic_data_landing_page(
    work_ctx, focus_on_synthetic_data, saas_potential_explanation, **kwargs
):
    logger.info(f"Executing task: create_synthetic_data_landing_page")

    prompt = """Please continue to act as an expert in SEO & eCommerce and Competitive Intelligence but also an expert on 
    Generative AI. ADSC created a small page on Generative AI on their website at 
    https://www.adscke.com/index.php/adsc-sales-marketing-generative-ai-services/ please review this. And then 
    knowing that ADSC is one of the few companies in the world that can use competitive intelligence and resulting 
    competitive insight from Generative AI together with human subject matter experts please generate at least a 
    five-page sub-website that explains the power of generative AI and how ADSC can help with it’s partners to create 
    custom Generative AI Agents. ADSC uses synthetic data for anything external. Please explain why that’s important. 
    And how this is about compliance from a privacy perspective. And talk both about internal Custom Agents to better 
    support sales and marketing and other complex business processes to save budget and increase sales. And then talk 
    about how there is the potential for SAAS sales of subscriptions for insights wrapped as custom Agents with 
    Synthetic Data. Synthetic Data needs to have it’s own page and should be linked into both the internal and 
    external pages talking about custom Agents. And please make sure that there is an appropriate styling to fit 
    WordPress and the current other pages in the ADSC website. And then output the HTML so that we can implement what 
    you’ve generated."""

    await create_tailwind_landing(prompt=prompt, filepath="synthetic_data_landing.html")

    return {
        "success": True,
        "results": f"Successfully executed: create_synthetic_data_landing_page",
    }


@register_task
async def confirm_interest_in_consultation(
    work_ctx, response_type, reasons_count, **kwargs
):
    logger.info(f"Executing task: confirm_interest_in_consultation")

    landing_prompt = f"""
thanking them for their inquiry and confirming that we will help to make them more competitive
    """

    # await create_tailwind_landing(prompt=landing_prompt, filepath="/Users/candacechatman/dev/shipit/build/confirm.html")

    return {
        "success": True,
        "results": f"Successfully executed: confirm_interest_in_consultation",
    }


@register_task
async def rewrite_ethical_CI_webpage(
    work_ctx, source_url, target_format, audience_focus, **kwargs
):
    logger.info(f"Executing task: rewrite_ethical_CI_webpage")

    landing_prompt = f"""
We all need to somehow use rubber-hits-the-road real-world understanding of what’s going on right now.

Unfortunately, the prospects & clients you speak to might not necessarily always be as forth coming as you might wish.

And competitors will want to be cagey around you to protect their interests.

And nothing else that can affect your business is usually just simple. Everything in a complex market is complicated. Finding meaning in that kind of environment can be quite challenging.

Add to this the growing trend by governments worldwide to increase privacy and now things have gotten more complicated.

You can use the Internet. However, there have been lawsuits written about publicly for those that trespassed on competitor’s websites.

And even knowing what to look at that might be relevant can for many groups starting from scratch or even enhancing an existing Competitive Intelligence program be a real issue.

So, there are a number of challenges including those above & others. Next let’s take a look at solutions.

Solutions That Can Make A Holistic Difference

There is a deep & rich & very powerful way of knowing what’s going on that might affect your business.

There are three things that we can teach about & also alternatively support on that might make a serious knowledge acquisition difference:

OSI – Open-Source Intelligence. The use of publicly available information to provide points of information that when taken together might yield some insight.
The Use of Front-Line Personnel. Using front-line personnel can yield information that otherwise might be missed & can be extremely valuable to the whole insight process.
Advanced Analysis Techniques. If a business is small enough sophisticated manual analysis techniques might suffice. For any company of size, the use of analytics (automated means of analysis) from easy-to-use Data Science platforms to Generative AI can make a difference. And we can suggest how to use such technologies whether from costly commercial offerings or free open-source software.
You might be wondering how that all these might fit together?

The Hidden Numbers Between The Words People Use Can Make All The Difference.

What numbers might we be referring to?

Not everything is obvious. But when you experience things in the right way it might be obvious as to its meaning.

We take a statistical, approach to this.

When there are different words or phrases, or events within a sales or marketing/customer success/support cycle that occur that repeat, these can be used as forensic clues as to what the meaning in the moment actually is.

So, when we hear repeating words or phrases or experience from some kind of significant event, we can quickly record this. And it can be quite useful.

A good example is that when we hear from a client or prospect that their budgets are frozen for a 60day period what they are usually saying without saying overtly (about 90% or more of the time), is that they are being acquired, we can then use tools & OSI to discover who might be acquiring them & sell into their bosses’ bosses.

This kind of scenario becomes a pattern, which is a kind of niche KPI. Essentially, we find an obstacle & by the recognition of this obstruction & by the recognition of it’s existence we gain a path to mitigate risk & over come it.

There are many other patterns & anti-patterns that we’ve discovered over the years. So, life quite often functions in a patterned or in other words relatively discernable organized repeating way. The repetitions might be different & connected to other repeating patterns. But the essentials are there. We can discern some meaning from something significant occurring.

The patterns may be too big or too small for us to easily see & understand.

So, that’s where using analytics of different sorts can be extremely useful.

        """

    await create_tailwind_landing(
        prompt=landing_prompt,
        filepath="/Users/candacechatman/dev/shipit/build/ethical_ci.html",
    )

    return {
        "success": True,
        "results": f"Successfully executed: rewrite_ethical_CI_webpage",
    }


@register_task
async def develop_generative_AI_mini_website(
    work_ctx, pages_count, focus_areas, wordpress_compatibility, **kwargs
):
    logger.info(f"Executing task: develop_generative_AI_mini_website")

    page_one = """Generative AI, also known as generative adversarial networks (GANs) or transformer models like GPT-3, is a groundbreaking technology that has transformed various fields. It enables machines to generate content, such as text, images, and even videos, that is often indistinguishable from human-created content. This technology relies on large datasets and advanced algorithms to learn and mimic the patterns, styles, and structures present in the training data.

The power of generative AI lies in its ability to create realistic and diverse content. In the context of text generation, it can be used to automate content creation, assist with creative writing, generate human-like responses in chatbots, and even aid in language translation. However, it also raises ethical and privacy concerns, as it can potentially be used to create fake news, deepfakes, and other forms of disinformation."""
    page_two = """Custom generative AI agents refer to AI systems that are tailored to specific tasks or domains. These agents are trained on specialized datasets and fine-tuned to excel in particular applications. For example, in healthcare, custom generative AI agents can be developed to generate medical reports, assist in diagnosis, or even simulate patient interactions for medical training.

The advantage of custom generative AI agents is their ability to provide highly specialized and accurate results within their domain. However, /Users/candacechatman/dev/shipit/building and fine-tuning these agents often require substantial expertise and domain-specific data."""
    page_three = """Synthetic data is artificially generated data that simulates real-world data. Generative AI plays a crucial role in creating synthetic data by mimicking the statistical patterns and structures of actual data. This synthetic data can be used for various purposes, including training machine learning models, testing algorithms, and ensuring data privacy.

One of the key advantages of synthetic data is that it allows organizations to work with sensitive or confidential information without exposing real data. It is particularly valuable in industries like healthcare and finance, where data privacy regulations are stringent. Additionally, synthetic data can be generated at scale, providing researchers and data scientists with a versatile tool for experimentation."""
    page_four = """Privacy compliance is a critical aspect of data management, especially in the age of AI and data-driven decision-making. Generative AI can both pose privacy challenges and offer solutions for privacy compliance.

On one hand, generative AI can be used to anonymize data by generating synthetic versions of sensitive data, ensuring that individuals' personal information remains protected while still allowing for meaningful analysis. On the other hand, there are concerns that generative AI can be used maliciously to de-anonymize data or create fake identities.

Navigating the complex landscape of privacy compliance in the context of AI requires a deep understanding of data protection regulations and responsible AI practices."""
    page_five = """Internal custom agents refer to AI systems designed for specific internal business operations within an organization. These agents can streamline workflows, automate repetitive tasks, and enhance decision-making processes.

For example, an internal custom agent in a customer service department might use natural language processing (NLP) to analyze customer inquiries and provide automated responses or route inquiries to the appropriate department. In manufacturing, custom AI agents can optimize supply chain logistics, predict equipment maintenance needs, and improve quality control.

These agents are tailored to the unique needs and processes of an organization, leveraging AI to increase efficiency and productivity. However, their development and integration require a deep understanding of the organization's operations and data flows.

In summary, generative AI and custom AI agents have the potential to transform various aspects of our lives, from content generation to data privacy and internal operations. While they offer significant benefits, their responsible development and use are essential to address ethical, privacy, and security concerns."""

    await create_tailwind_landing(
        prompt=page_one, filepath="/Users/candacechatman/dev/shipit/build/page_one.html"
    )
    await create_tailwind_landing(
        prompt=page_two, filepath="/Users/candacechatman/dev/shipit/build/page_two.html"
    )
    await create_tailwind_landing(
        prompt=page_three,
        filepath="/Users/candacechatman/dev/shipit/build/page_three.html",
    )
    await create_tailwind_landing(
        prompt=page_four,
        filepath="/Users/candacechatman/dev/shipit/build/page_four.html",
    )
    await create_tailwind_landing(
        prompt=page_five,
        filepath="/Users/candacechatman/dev/shipit/build/page_five.html",
    )

    return {
        "success": True,
        "results": f"Successfully executed: develop_generative_AI_mini_website",
    }


async def main():
    # await competitive_analysis_ADSC(work_ctx=None, services=None, revenue_threshold=None)
    # await create_landing_page_CI_AI_services(None, emphasize_CI=None, target_audience=None, call_to_action=None)
    # await generate_follow_up_forms(None, description=None, question_types=None, response_based_branching=None)
    # await create_synthetic_data_landing_page(None, focus_on_synthetic_data=None, saas_potential_explanation=None)
    # await confirm_interest_in_consultation(None, response_type=None, reasons_count=None)
    # await rewrite_ethical_CI_webpage(None, source_url=None, target_format=None, audience_focus=None)
    await develop_generative_AI_mini_website(
        None, pages_count=None, focus_areas=None, wordpress_compatibility=None
    )


if __name__ == "__main__":
    anyio.run(main)
