from asyncio import ensure_future
from functools import cache

from playwright.async_api import async_playwright
from promptools.openai import count_token


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

    browser = await p.chromium.launch()
    print(browser)

    page = await browser.new_page()
    print(page)

    await page.goto(url, wait_until="domcontentloaded")
    print(page)
    await page.evaluate(
        "scrollTo({ top: document.body.scrollHeight / 4, behavior: 'smooth' })",
    )
    # await page.wait_for_load_state("networkidle")
    await page.wait_for_load_state("load")
    html = await page.content()

    print(f"{count_token(html) = }")
    ensure_future(page.close())  # noqa: RUF006
    return html
