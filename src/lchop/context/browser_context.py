import asyncio
import functools
import json
from dataclasses import dataclass

import requests
from loguru import logger
from pyppeteer import connect, launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page


def with_delay(delay_seconds=1):  # Set default delay to 1 second
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info(f"Waiting {delay_seconds} seconds...")
            await asyncio.sleep(delay_seconds)
            logger.info(f"Continuing...")
            return await func(*args, **kwargs)

        return wrapper

    return decorator


@dataclass
class BrowserContext:
    use_existing_browser: bool = False
    enable_request_interception: bool = False
    browser: Browser = None
    page: Page = None

    async def launch_browser(self, **kwargs):
        try:
            ws_url = self.get_ws_url()
            if ws_url:
                self.browser = await connect(browserWSEndpoint=ws_url)
            else:
                self.browser = await launch()
            self.page = (await self.browser.pages())[0]
            logger.info("Browser launched.")

            if self.enable_request_interception:
                await self.setup_request_interception()
        except ConnectionError as e:
            logger.error(
                f"Failed to launch the browser: {e}\nDid you start it with "
                f"`google-chrome --remote-debugging-port=9222`?"
            )
            raise

        # Verifying the connection to the browser and page
        if self.browser and self.page:
            logger.info("Verified connection to browser and page.")
        else:
            logger.error("Browser and/or page connection could not be verified.")
            raise Exception("Browser and/or page connection verification failed.")

    async def setup_request_interception(self):
        try:
            await self.page.setRequestInterception(True)
            self.page.on("request", self.intercept_request)
            logger.info("Request interception set up.")
        except Exception as e:
            logger.error(f"Failed to set up request interception: {e}")
            raise

    async def intercept_request(self, intercepted_request):
        try:
            # if intercepted_request.resourceType in ['image', 'stylesheet', 'font']:
            # await intercepted_request.abort()
            # else:
            await intercepted_request.continue_()
        except Exception as e:
            logger.error(f"Failed to intercept request: {e}")
            raise

    async def close_browser(self):
        try:
            await self.browser.close()
            logger.info("Browser closed.")
        except Exception as e:
            logger.error(f"Failed to close the browser: {e}")
            raise

    def get_ws_url(self):
        try:
            if self.use_existing_browser:
                response = requests.get("http://localhost:9222/json/version")
                ws_url = json.loads(response.text)["webSocketDebuggerUrl"]
                return ws_url
        except Exception as e:
            logger.error(f"Failed to get WebSocket URL: {e}")
            raise


if __name__ == "__main__":
    ctx = BrowserContext(use_existing_browser=True, enable_request_interception=True)
    asyncio.get_event_loop().run_until_complete(ctx.launch_browser())
    # Do some actions with the page and intercepted requests
    asyncio.get_event_loop().run_until_complete(ctx.close_browser())
