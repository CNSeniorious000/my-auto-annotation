from contextlib import suppress

with suppress(ImportError):
    from dotenv import load_dotenv

    load_dotenv(verbose=True, override=True)
