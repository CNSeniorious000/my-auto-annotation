from json import loads

from cssselect import SelectorSyntaxError
from parsel import Selector
from promplate import Callback, ChainContext, Context, Jump, Loop, Node

from ..templates import one_pass
from ..utils.browser import fetch
from ..utils.dom import remove_attrib, show
from ..utils.log import print_exception_only, print_label
from ..utils.uuid import replace_uuids

main_loop = Loop(first_pass := Node(one_pass, response_format={"type": "json_object"}))


@first_pass.callback
class _(Callback):
    async def pre_process(self, context: Context):
        html = await fetch("http://ws.sdnews.com.cn/ft/202405/t20240525_4392444.htm")
        html = replace_uuids(html)

        dom = self.dom = Selector(html)

        dom.css("script, noscript, iframe, style, img[src^='data:'], svg").drop()

        for i in dom.css("[style]"):
            remove_attrib(i, "style")

        for i in dom.css("img[src][srcset]"):
            remove_attrib(i, "srcset")

        context["html"] = dom.css("body").get()

    async def end_process(self, context: ChainContext):
        res: dict[str, str | None] = loads(context.result)
        success = True

        for key, selector in res.items():
            if selector:
                print_label(f"{key} - {selector}")
                try:
                    results = self.dom.css(selector)
                    if not results:
                        success = False
                    show(results)
                except SelectorSyntaxError as e:
                    print_exception_only(e)
                    success = False

        if success:
            raise Jump(out_of=main_loop)
