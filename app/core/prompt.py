from json import loads
from traceback import format_exception_only

from cssselect import SelectorSyntaxError
from parsel import Selector
from promplate import Callback, ChainContext, Jump, Loop, Node

from ..templates import prompt
from ..utils.dom import show
from ..utils.log import print_exception_only, print_label

main_loop = Loop(each := Node(prompt, response_format={"type": "json_object"}))


@each.callback
class _(Callback):  # noqa: N801
    max_retries = 4

    async def end_process(self, context: ChainContext):
        dom: Selector = context["dom"]

        res: dict[str, str | None] = loads(context.result)
        problems = context["problems"] = []

        for key, selector in res.items():
            if selector:
                print_label(f"{key} - {selector}")
                try:
                    if results := dom.css(selector):
                        show(results)
                    elif self.max_retries:
                        problems.append((key, None))
                    else:
                        res[key] = None

                except SelectorSyntaxError as e:
                    print_exception_only(e)
                    problems.append((key, format_exception_only(e)))

        if not problems or not self.max_retries:
            raise Jump(out_of=main_loop)

        self.max_retries -= 1
