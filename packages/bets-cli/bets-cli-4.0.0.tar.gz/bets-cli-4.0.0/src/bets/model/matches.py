from pathlib import Path
from random import randint
from typing import Dict, Iterable, Tuple, Optional

from tabulate import tabulate

from bets.utils import log
from bets.utils.decorators import cachedproperty
from bets.utils.string_utils import fmt_tuple, randstr, split_lines

COLUMNS = ("1", "X", "2", "[1]", "[x]", "[2]", "min", "med", "max", "Title")
OUTCOMES = ("1", "X", "2")
RANKS = ("min", "med", "max")


def get_ranks(first: float, second: float, third: float) -> Tuple[str, str, str]:
    """Gets the ranks of 3 values.
    Examples:
        >>> get_ranks(1,2,3)
        ('min', 'med', 'max')
        >>> get_ranks(1,2,2)
        ('min', 'med/max', 'med/max')
    """

    all_ratios = (first, second, third)
    sorted_ratios = list(sorted(all_ratios))

    ranks = []
    for idx, ratio in enumerate(all_ratios):
        ratio_ranks = []

        for sorted_ratio, rank in zip(sorted_ratios, ("min", "med", "max")):
            if ratio == sorted_ratio:
                ratio_ranks.append(rank)

        ranks.append("/".join(ratio_ranks))
    log.debug(f"ranks of: {all_ratios} -> {ranks}")
    return tuple(ranks)


def randratio() -> float:
    int_part = randint(1, 9)
    float_part = randint(10, 99)
    return float(f"{int_part}.{float_part}")


class Match:
    title: str
    ratios: Tuple[float, float, float]
    ranks: Tuple[str, str, str]
    outcome2ratio: Dict[str, float]
    outcome2rank: Dict[str, str]
    rank2outcome: Dict[str, str]

    def __init__(self, *args):
        if len(args) < 4:
            raise ValueError(f"Expected a least 4 args, Got [{len(args)}]: {args}")
        self.title = args[0]
        self.ratios = tuple(float(float(arg).__format__(".2f")) for arg in args[1:4])
        self.ranks = get_ranks(*self.ratios)
        self.outcome2ratio = {outcome: ratio for outcome, ratio in zip(OUTCOMES, self.ratios)}
        self.outcome2rank = {outcome: rank for outcome, rank in zip(OUTCOMES, self.ranks)}
        self.rank2outcome = {value: key for key, value in self.outcome2rank.items()}

    def __eq__(self, other):
        if isinstance(other, Match):
            return (self.title == other.title
                    and self.ratios == other.ratios)
        return False

    def __getitem__(self, item):
        if item in OUTCOMES:  # pass outcome get ratio
            return self.outcome2ratio[item]

        if item in RANKS:  # pass rank get outcome
            if item in self.rank2outcome:
                return self.rank2outcome[item]

            outcomes = []
            print(f"item: {item} , rank2outcome: {self.rank2outcome}")
            for outcome, rank in self.outcome2rank.items():
                if item in rank:
                    outcomes.append(outcome)

            return "/".join(outcomes)

        raise KeyError(item, list(self.rank2outcome.keys()))

    def __repr__(self):
        return f"Match('{self.title}', {self['1']}, {self['X']}, {self['2']})"

    def __str__(self):
        return str(self.tuple)

    @cachedproperty
    def tuple(self) -> tuple:
        return self.ratios + self.ranks + (self["min"], self["med"], self["max"]) + (self.title,)

    @cachedproperty
    def dict(self) -> dict:
        return {key: value for key, value in zip(COLUMNS, self.tuple)}

    @cachedproperty
    def csv(self) -> str:
        return ",".join(fmt_tuple(self.tuple).split(maxsplit=9))

    @cachedproperty
    def columns(self):
        return [COLUMNS[-1]] + list(COLUMNS[:-1])

    @cachedproperty
    def values(self):
        data = fmt_tuple(self.tuple).split(maxsplit=9)
        return [data[-1]] + data[:-1]

    @classmethod
    def random(cls) -> "Match":
        host = randstr(5, 15).capitalize()
        guest = randstr(5, 15).capitalize()
        title = f"{host} - {guest}"
        r1 = randratio()
        rx = randratio()
        r2 = randratio()
        return cls(title, r1, rx, r2)


def _parse_efbet(text: str) -> "Matches":
    lines = split_lines(text)

    def _get_title_index(start_line=0):
        for i, line in enumerate(lines):
            if i < start_line:
                continue
            if "vs" in line:
                return i
        raise ValueError("lines don't contain efbet match title (no 'vs')!")

    title_index = _get_title_index()
    ratio_1_index = title_index + 1
    ratio_x_index = ratio_1_index + 1
    ratio_2_index = ratio_x_index + 1
    second_title_index = _get_title_index(ratio_2_index)
    record_size = second_title_index - title_index

    titles = lines[title_index::record_size]
    ratios_1 = lines[ratio_1_index::record_size]
    ratios_x = lines[ratio_x_index::record_size]
    ratios_2 = lines[ratio_2_index::record_size]

    return Matches(Match(title, r1, rx, r2) for title, r1, rx, r2 in zip(titles, ratios_1, ratios_x, ratios_2))


def _parse_lines(text: str) -> "Matches":
    lines = split_lines(text)

    def parse_line(line: str) -> Match:
        line_parts = line.strip().split(" ")
        if len(line_parts) < 4:
            raise ValueError("Line should contain at least 4 space-separated parts! 'title r1 rx r2'")
        title = " ".join(line_parts[:-3])
        r1, rx, r2 = line_parts[-3:]
        return Match(title, r1, rx, r2)

    return Matches(parse_line(line) for line in lines)


class Matches:
    PARSERS = {
        "efbet": _parse_efbet,
        "lines": _parse_lines
    }

    def __init__(self, matches: Iterable[Match] = None):
        self._matches = list(matches) if bool(matches) else []

    def __eq__(self, other):
        if isinstance(other, Matches):
            return self._matches == other._matches
        if isinstance(other, list):
            return self._matches == other
        return False

    def __contains__(self, item):
        if isinstance(item, Match):
            return item in self._matches
        if isinstance(item, str):
            return bool([m for m in self._matches if m.title == item])
        raise TypeError("Expected Match or str!", item)

    def __len__(self):
        return self._matches.__len__()

    def __iter__(self):
        return self._matches.__iter__()

    def __getitem__(self, item) -> Optional[Match]:
        if isinstance(item, int):
            return self._matches[item]

        if isinstance(item, str):
            for m in self._matches:
                if m.title == item:
                    return m
            return None

        raise KeyError(item)

    def __str__(self):
        return self.table

    def __bool__(self):
        return bool(self._matches)

    @cachedproperty
    def columns(self):
        return [COLUMNS[-1]] + list(COLUMNS[:-1])

    def append(self, match: Match):
        if not isinstance(match, Match):
            raise TypeError("Expected Match!", match)
        self._matches.append(match)

    def add_match(self, title, ratio1, ratiox, ratio2):
        self.append(Match(title, ratio1, ratiox, ratio2))

    def extend(self, matches: Iterable[Match]):
        for match in matches:
            self.append(match)

    @property
    def csv(self) -> str:
        header = ",".join(COLUMNS)
        data = "\n".join(m.csv for m in self)
        return f"{header}\n{data}"

    @property
    def table(self) -> str:
        return tabulate(
            tabular_data=[m.dict for m in self],
            showindex=list(range(1, len(self) + 1)),
            tablefmt="fancy_grid",
            headers="keys",
            stralign="center",
            numalign="decimal",
            floatfmt='.2f',
            disable_numparse=list(range(4, 10))
        )

    @classmethod
    def random(cls, size=5):
        instance = cls()
        instance.extend(Match.random() for _ in range(size))
        return instance

    def write_to_csv(self, file):
        Path(file).write_text(self.csv, encoding="utf-8")

    def write_to_txt(self, file):
        Path(file).write_text(self.table, encoding="utf-8")

    def write_to_file(self, file: str):
        file_ext = file[file.rfind(".") + 1:].lower()
        write_func = self.write_to_csv if file_ext == "csv" else self.write_to_txt
        write_func(file)

    def clear(self):
        self._matches.clear()
