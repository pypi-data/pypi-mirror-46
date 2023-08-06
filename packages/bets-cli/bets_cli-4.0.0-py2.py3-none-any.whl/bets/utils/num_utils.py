import logging

from itertools import product
from typing import Iterable, Union

_log = logging.getLogger(__name__)


def parse_float(value: Union[int, float, str]) -> float:
    _log.debug("parsing [{}] to float...".format(value))
    try:
        return float(value)
    except (ValueError, TypeError):
        if isinstance(value, str):
            value = value.strip().replace(" ", "")

            try:
                return float(value)

            except (ValueError, TypeError):
                if "," in value:
                    if "." in value:
                        return float(value.replace(",", ""))

                    return float(value.replace(",", "."))

        raise ValueError(f"Could not parse value to float", value)


def generate_variations(items, length: int):
    _log.info("generating all variations of size [{}] consisting of [{}]".format(length, items))
    for variation in product(items, repeat=length):
        yield variation


def multiply_all(items: Iterable[Union[int, float]]) -> float:
    result = 1
    for i in items:
        result = result * i
    return result
