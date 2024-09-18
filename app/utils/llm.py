from promplate.llm.openai import AsyncChatGenerate
from rich.color import Color
from rich.console import Console
from rich.style import Style

from .log import print_token_usage

generate = AsyncChatGenerate().bind(model="gpt-4o-mini")


console = Console()


style_gen = Style(
    color=Color.from_rgb(255, 255, 255),
    bgcolor=Color.from_rgb(60, 66, 78),
)


async def complete(prompt, **kwargs):
    console.print(prompt, style="dim")
    print("<|assistant|>")

    res = ""
    async for i in generate(prompt, **kwargs):
        if i:
            res += i
            console.print(i, end="", style=style_gen)

    print()

    print_token_usage(prompt, res)

    return res
