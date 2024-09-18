from asyncio import ensure_future
from contextlib import suppress
from functools import cache

from playwright.async_api import TimeoutError, async_playwright


async def _make_instance():
    return await async_playwright().start()


@cache
def get_instance():
    return ensure_future(_make_instance())


async def cleanup():
    playwright = await get_instance()
    await playwright.stop()


async def fetch(url: str):
    p = await get_instance()

    browser = await p.chromium.launch(headless=False)
    print(browser)

    page = await browser.new_page()
    print(page)

    await page.goto(url, wait_until="domcontentloaded")
    print(page)
    await page.evaluate(
        "scrollTo({ top: document.body.scrollHeight / 4, behavior: 'smooth' })",
    )
    # await page.wait_for_load_state("networkidle")
    with suppress(TimeoutError):
        await page.wait_for_load_state("load")

    return page
