from parsel import Selector

from app.utils.browser import fetch

from ..utils.dom import remove_attrib
from ..utils.uuid import replace_uuids


async def get_cleaned_dom(url: str):
    html = await fetch(url)
    html = replace_uuids(html)

    dom = Selector(html)

    dom.css("script, noscript, iframe, style, img[src^='data:'], svg").drop()

    for i in dom.css("[style]"):
        remove_attrib(i, "style")

    for i in dom.css("img[src][srcset]"):
        remove_attrib(i, "srcset")

    return dom
