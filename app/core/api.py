from json import loads

from ..utils.dom import compress_spaces
from ..utils.llm import complete
from .parse import get_cleaned_dom
from .prompt import main_loop


async def auto_annotate(url: str) -> dict[str, str]:
    dom = await get_cleaned_dom(url)

    context = await main_loop.ainvoke(
        {
            "dom": dom,
            "html": compress_spaces(dom.css("body").get()),  # type: ignore
        },
        complete=complete,
        temperature=0,
    )

    return loads(context.result)
