from typing import Hashable, Any


def extract(source: dict[Hashable, Any], keys: tuple[Hashable]) -> dict[Hashable, Any]:
    return {k: v for k, v in source.items() if k not in keys}
