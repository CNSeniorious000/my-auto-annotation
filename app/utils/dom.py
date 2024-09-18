from lxml.html import HtmlElement
from parsel import Selector, SelectorList

from .log import print_results


def show(selector: Selector | SelectorList):
    text = " ".join(selector.css("::text").extract()).strip()
    if text:
        print_results(text)
    else:
        print_results(" ".join(selector.extract()).strip(), highlight=True)


def remove_attrib(selector: Selector, attribute_name: str):
    element: HtmlElement = selector.root
    element.attrib.pop(attribute_name)
