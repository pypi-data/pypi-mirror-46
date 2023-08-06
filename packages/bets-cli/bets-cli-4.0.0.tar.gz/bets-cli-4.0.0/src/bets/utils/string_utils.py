from csv import DictWriter
from io import StringIO
from typing import List, Dict, Any
from random import choice, randint
from string import ascii_letters

OUTCOMES = tuple("1 X 2".split())
RANKS = tuple("min med max".split())


def _fmt_float(value: float) -> str:
    return value.__format__(".2f")


def _fmt_int(value: int) -> str:
    return str(value)


def _fmt_str(value: str) -> str:
    for rank in RANKS:
        if rank in value:
            return value.center(7)
    if value in OUTCOMES:
        return value
    return value


def _fmt_value(value) -> str:
    fmt_funcs = {
        "int": _fmt_int,
        "float": _fmt_float,
        "str": _fmt_str
    }
    return fmt_funcs[type(value).__name__](value)


def fmt_tuple(tpl: tuple):
    return " ".join([_fmt_value(value) for value in tpl])


def split_lines(text: str) -> List[str]:
    return [line.strip()
            for line
            in text.strip().split("\n")
            if line.strip()]


def randstr(min_size: int, max_size: int) -> str:
    return "".join(choice(ascii_letters) for _ in range(randint(min_size, max_size)))


def csv_from_dicts(dicts: List[Dict[str, Any]], columns: List[str] = None):
    if not dicts:
        raise ValueError("Empty list!")

    columns = columns or list(dicts[0].keys())

    buffer = StringIO()
    writer = DictWriter(buffer, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for item in dicts:
        writer.writerow(item)

    return buffer.getvalue()
