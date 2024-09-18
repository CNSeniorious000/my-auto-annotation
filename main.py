from traceback import print_exception

from app.core.prompt import main_loop
from app.utils.browser import cleanup
from app.utils.llm import complete
from app.utils.loop import get_event_loop


async def main():
    try:
        res = await main_loop.ainvoke(complete=complete)
        _ = res
    except Exception as e:
        print_exception(e)
        await cleanup()


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())
