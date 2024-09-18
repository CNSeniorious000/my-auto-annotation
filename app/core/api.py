from json import loads

from promptools.openai import count_token

from ..utils.dom import compress_spaces
from ..utils.llm import complete
from .parse import get_cleaned_dom
from .prompt import main_loop

MAX_TOKENS = 40_000


async def auto_annotate(url: str) -> dict[str, str]:
    dom = await get_cleaned_dom(url)
    html = compress_spaces(dom.css("body").get())  # type: ignore

    if count_token(html) > MAX_TOKENS:
        return {}

    context = await main_loop.ainvoke(
        {"dom": dom, "html": html},
        complete=complete,
        temperature=0,
    )

    return loads(context.result)
