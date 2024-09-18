from asyncio import get_running_loop, new_event_loop


def get_event_loop():
    try:
        return get_running_loop()
    except RuntimeError:
        return new_event_loop()
