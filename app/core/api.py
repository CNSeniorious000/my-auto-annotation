from asyncio import ensure_future
from json import dumps, loads
from pathlib import Path
from typing import TypedDict, cast

from promptools.openai import count_token

from ..utils.browser import fetch
from ..utils.css import merge_computed_styes
from ..utils.dom import compress_spaces
from ..utils.find import find_urls_in_json
from ..utils.llm import complete
from .parse import get_cleaned_dom
from .prompt import main_loop

MAX_TOKENS = 40_000


async def auto_annotate(url: str):
    page = await fetch(url)
    html = await page.content()
    dom = await get_cleaned_dom(html)
    body = compress_spaces(dom.css("body").get())  # type: ignore

    html_tokens = count_token(html)
    body_tokens = count_token(body)

    print(f" Page HTML {html_tokens} -> {body_tokens} tokens")

    if body_tokens > MAX_TOKENS:
        ensure_future(page.close())  # noqa: RUF006
        return

    context = await main_loop.ainvoke(
        {"page": page, "dom": dom, "html": body},
        complete=complete,
        temperature=0,
    )

    result: dict[str, ResultItem] = {}

    for task, selector in cast(dict[str, str | None], loads(context.result).items()):
        if not selector:
            continue

        computed_styles = await page.eval_on_selector_all(
            selector,
            """
                elements => {
                    // 获得所有的 computedStyle
                    const results = [];
                    for (const element of elements) {
                        const style = getComputedStyle(element);
                        const styleObj = {};
                        for (let i = 0; i < style.length; i++) {
                            const name = style[i];
                            styleObj[name] = style.getPropertyValue(name);
                        }
                        results.push(styleObj);
                    }
                    return results;
                }
            """,
        )
        merged_style = merge_computed_styes(computed_styles)
        result[task] = {
            "selector": selector,
            "html": dom.css(selector).extract(),
            "style": merged_style,
        }

    ensure_future(page.close())  # noqa: RUF006

    return result


class ResultItem(TypedDict):
    selector: str
    html: list[str]
    style: dict[str, str]


async def auto_annotation_file(path_in: str, path_out: str):
    urls = find_urls_in_json(Path(path_in).read_text("utf-8"))
    results = {url: await auto_annotate(url) for url in urls}
    Path(path_out).write_text(dumps(results, ensure_ascii=False), "utf-8")
