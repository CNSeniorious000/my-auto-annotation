import re
from json import loads


def find_urls_in_json(text: str) -> list[str]:
    return list(map(loads, re.findall(r'"https?://[^\s]+"', text)))
