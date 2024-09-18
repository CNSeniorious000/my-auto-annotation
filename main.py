from json import loads
from pathlib import Path
from traceback import print_exception

from app.core.api import auto_annotate
from app.utils.browser import cleanup
from app.utils.loop import get_event_loop

tasks = [i["url"] for i in loads(Path("task1.json").read_text("utf-8"))["tasks"]]


async def main():
    try:
        for i in range(499, 505):
            res = await auto_annotate(tasks[i])
            _ = res
    except Exception as e:
        print_exception(e)
        await cleanup()


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())
