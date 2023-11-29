import asyncio
import functools
from urllib.parse import quote, urlencode

from bs4 import BeautifulSoup
from loguru import logger

from lchop.context.browser_context import with_delay
from lchop.context.task_context import register_task


@register_task
async def hello_world_template(work_ctx, **kwargs):
    try:
        # Extracting the TemplateContext
        template_ctx = work_ctx.template_ctx

        # Define the template string
        template_str = "Hello {{ world_var }}!"

        # Set a global variable in the template context
        template_ctx.set_variable("world_var", "World")

        # Render the template
        rendered_str = template_ctx.render_template(template_str)

        logger.info(f"Successfully rendered the hello world command: {rendered_str}")

        return rendered_str

    except Exception as e:
        logger.error(f"Failed to execute the hello world command: {str(e)}")
        raise


@with_delay()
@register_task
async def navigate_to_url(work_ctx, url, **kwargs):
    try:
        page = work_ctx.browser_ctx.page
        await page.goto(url)
        logger.info(f"Navigated to URL: {url}")
    except Exception as e:
        logger.error(f"Failed to navigate to URL: {str(e)}")
        raise


@with_delay
@register_task
async def click_element(work_ctx, selector, **kwargs):
    try:
        browser_ctx = work_ctx.browser_ctx

        await browser_ctx.page.click(selector)
        logger.info(f"Clicked element: {selector}")
    except Exception as e:
        logger.error(f"Failed to click element: {str(e)}")
        raise


@with_delay
@register_task
async def fill_linkedin(work_ctx, selector, value, **kwargs):
    try:
        browser_ctx = work_ctx.browser_ctx
        page = browser_ctx.page
        await page.type(selector, value)
        logger.info(f"Filled form field {selector} with value {value}")
    except Exception as e:
        logger.error(f"Failed to fill form: {str(e)}")
        raise


def sales_nav_url(keywords):
    base_url = "https://www.linkedin.com/sales/search/people"
    search_query = f"(spellCorrectionEnabled:true,keywords:{keywords})"
    query_kwargs = {"query": search_query}
    encoded_query = urlencode(query_kwargs, quote_via=quote)
    full_url = f"{base_url}?{encoded_query}"
    return full_url


def group_url(group_id):
    base_url = "https://www.linkedin.com/groups"
    full_url = f"{base_url}/{group_id}/"
    return full_url


def group_members_url(group_id):
    full_url = f"{group_url(group_id)}/members/"
    return full_url


def success(results=None):
    return {"success": True, "results": f"{results}"}


@with_delay
@register_task
async def navigate_to_group_members(work_ctx, group_id, **kwargs):
    page = work_ctx.browser_ctx.page

    await page.goto(group_members_url(group_id))
    return success("Navigated to group members page.")


@register_task
async def search_ln_sales_nav(work_ctx, keywords, **kwargs):
    page = work_ctx.browser_ctx.page

    await page.goto(sales_nav_url(keywords))


@register_task
async def scrape_ln_sales_nav(work_ctx, **kwargs):
    # Get the page source from browser context
    page = work_ctx.browser_ctx.page
    page_source = await page.content()
    # find the users phone number using bs and regex
    bs = BeautifulSoup(page_source, "html.parser")
    phone_number = bs.find("a", {"class": "ember-view link-without-visited-state"})
    phone_number = phone_number.text
    # find the users email using bs and regex
    email = bs.find("a", {"class": "ember-view link-without-visited-state"})
    email = email.text
    # find the users name using bs and regex
    name = bs.find("span", {"class": "name actor-name"})
    name = name.text
    # find the users company using bs and regex
    company = bs.find("span", {"class": "company-name"})
    company = company.text
    # find the users position using bs and regex


@register_task
async def detect_recession(work_ctx, **kwargs):
    # Go to the census website
    page = work_ctx.browser_ctx.page
    await page.goto("https://www.census.gov/economic-indicators/")


class LinkedInGroup:
    name: str


class LinkedInProfile:
    groups: list
    lastName: str
    memorialized: bool
    objectUrn: str
    geoRegion: str
    saved: bool
    openLink: bool
    premium: bool
    currentPositions: list
    entityUrn: str
    viewed: bool
    spotlightBadges: list
    trackingId: str
    blockThirdPartyDataSharing: bool
    summary: str
    pendingInvitation: bool
    pastPositions: list
    degree: int
    fullName: str
    listCount: int
    firstName: str
    profilePictureDisplayImage: dict
    profileLink: str

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@register_task
async def generate_profiles_page(task, work_ctx, **kwargs):
    data = task.profiles

    profiles = []

    for profile in data.elements:
        del profile["$recipeType"]
        del profile["$anti_abuse_metadata"]

        # create profile link
        urn = profile["entityUrn"].split(":")[3]
        urn = urn.replace("(", "")
        urn = urn.replace(")", "")
        profile["profileLink"] = f"https://www.linkedin.com/sales/lead/{urn}"

        pro = LinkedInProfile(**profile)
        profiles.append(pro)

    print(profiles[0].profilePictureDisplayImage)
    pro = profiles[0]
    full_img = (
        pro.profilePictureDisplayImage["rootUrl"]
        + pro.profilePictureDisplayImage["artifacts"][0][
            "fileIdentifyingUrlPathSegment"
        ]
    )
    print(full_img)
