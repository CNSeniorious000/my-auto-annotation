from asyncio import ensure_future
from json import loads

from promptools.openai import count_token

from ..utils.browser import fetch
from ..utils.dom import compress_spaces
from ..utils.llm import complete
from .parse import get_cleaned_dom
from .prompt import main_loop

MAX_TOKENS = 40_000


async def auto_annotate(url: str) -> dict[str, str]:
    page = await fetch(url)
    html = await page.content()
    dom = await get_cleaned_dom(html)
    body = compress_spaces(dom.css("body").get())  # type: ignore

    html_tokens = count_token(html)
    body_tokens = count_token(body)

    print(f" Page HTML {html_tokens} -> {body_tokens} tokens")

    if body_tokens > MAX_TOKENS:
        ensure_future(page.close())  # noqa: RUF006
        return {}

    context = await main_loop.ainvoke(
        {"page": page, "dom": dom, "html": body},
        complete=complete,
        temperature=0,
    )

    ensure_future(page.close())  # noqa: RUF006

    return loads(context.result)
