from json import loads
from pathlib import Path
from traceback import print_exception

from app.core.api import auto_annotation_file
from app.utils.browser import cleanup
from app.utils.loop import get_event_loop

tasks = [i["url"] for i in loads(Path("task1.json").read_text("utf-8"))["tasks"]]


async def main(file: str):
    try:
        await auto_annotation_file(file, "out.json")
    except Exception as e:
        print_exception(e)
    finally:
        await cleanup()


if __name__ == "__main__":
    from sys import argv

    loop = get_event_loop()
    loop.run_until_complete(main(argv[-1]))
