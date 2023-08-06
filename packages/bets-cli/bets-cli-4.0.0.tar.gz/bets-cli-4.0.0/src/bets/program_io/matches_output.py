import logging
from pathlib import Path
from typing import List

from tabulate import tabulate
from pandas import DataFrame

from bets.model.match import Match

_log = logging.getLogger(__name__)


def fmt_to_csv(matches: List[Match]) -> str:
    return DataFrame(
        data=(m.tuple for m in matches),
        columns=Match.COLUMNS
    ).to_csv(
        float_format="%.2f",
        columns=Match.COLUMNS,
        index=None
    )


def fmt_to_table(matches: List[Match], tablefmt: str) -> str:
    return tabulate(
        tabular_data=(m.tuple for m in matches),
        headers=Match.COLUMNS,
        floatfmt=".2f",
        stralign="center",
        disable_numparse=[4, 5, 6, -3, -2, -1],
        tablefmt=tablefmt,
        showindex=False
    )


class MatchesOutput:
    VALID_FORMATS = {"csv", "plain", "fancy_grid"}

    def __init__(self, matches: List[Match], out_dest="console", fmt="plain"):
        if (not isinstance(fmt, str)) or (fmt not in self.VALID_FORMATS):
            raise ValueError("Unsupported format [{}]".format(fmt), self.VALID_FORMATS)

        self.matches = matches
        self.out_dest = out_dest
        self.fmt = fmt

    @property
    def text(self) -> str:
        return fmt_to_csv(self.matches) if (self.fmt == "csv") else fmt_to_table(self.matches, self.fmt)

    def write(self):
        if self.out_dest == "console":
            print(self.text)
            return

        with Path(self.out_dest).open("wb") as fp:
            fp.write(self.text.encode("utf-8"))

    @classmethod
    def write_matches(cls, matches: List[Match], out_dest="console", fmt="plain"):
        cls(matches, out_dest, fmt).write()
