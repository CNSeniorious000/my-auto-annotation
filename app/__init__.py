from contextlib import suppress

with suppress(ImportError):
    from dotenv import load_dotenv  # type: ignore

    load_dotenv(verbose=True, override=True)
