import re

from lxml.html import HtmlElement
from parsel import Selector, SelectorList

from .log import print_results


def show(selector: Selector | SelectorList):
    if text := " ".join(selector.css("::text").extract()).strip():
        print_results(text)
    else:
        print_results(" ".join(selector.extract()).strip(), highlight=True)


def remove_attrib(selector: Selector, attribute_name: str):
    element: HtmlElement = selector.root
    element.attrib.pop(attribute_name)


sub_trailing_spaces = re.compile(r"\s+$", re.MULTILINE)
sub_multiple_lines = re.compile(r"\n{2,}")


def compress_spaces(html: str):
    html = html.replace("\r", "")
    html = sub_trailing_spaces.sub("", html)
    html = sub_multiple_lines.sub("\n", html)
    return html
