from collections import Counter


def merge_computed_styes(computed_styles: list[dict[str, str]]):
    counter = Counter()

    for style in computed_styles:
        counter.update([*style.items()])

    return dict(
        [pair for pair, count in counter.items() if count == len(computed_styles)]
    )
