from traceback import format_exception_only

from promptools.openai import count_token
from rich.console import Console

console = Console()


def print_token_usage(prompt, completion):
    from promplate.prompt.chat import ensure

    a = count_token(ensure(prompt))
    b = count_token(completion)
    c = a + b
    console.print(
        f"\n [r] usages [/r] {a} + {b} = {c} [green]$ {(a * 0.15 + b * 0.6) / 1_000} / 1k rounds",
        style="bright_red",
    )


def print_exception_only(exc: Exception):
    console.log(format_exception_only(exc), style="bright_red")


def print_label(label: str):
    console.print(f"\n [r] {label} [/r] ", end="", style="bright_magenta")


def print_results(content, highlight=False):
    console.print(content, style="bright_magenta", highlight=highlight)
