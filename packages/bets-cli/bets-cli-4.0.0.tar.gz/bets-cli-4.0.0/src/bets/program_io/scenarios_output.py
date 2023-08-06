import logging
from pathlib import Path
from typing import List

from pandas import DataFrame
from tabulate import tabulate

_log = logging.getLogger(__name__)


def fmt_to_table(scenarios: List[dict], tablefmt: str) -> str:
    return tabulate(scenarios,
                    headers="keys",
                    floatfmt=".2f",
                    stralign="center",
                    tablefmt=tablefmt)


def fmt_to_csv(scenarios: List[dict]):
    return DataFrame(
        scenarios,
        columns=list(scenarios[0].keys())
    ).to_csv(
        columns=list(scenarios[0].keys()),
        float_format="%.2f"
    )


class ScenariosOutput:
    VALID_FORMATS = {"csv", "plain", "fancy_grid"}

    def __init__(self, scenarios: List[dict], out_dest, out_fmt):
        if out_fmt not in self.VALID_FORMATS:
            raise ValueError("Unsupported format [{}]".format(out_fmt), self.VALID_FORMATS)
        self.scenarios = scenarios
        self.columns = list(self.scenarios[0].keys())
        self.out_dest = out_dest
        self.out_fmt = out_fmt

    @property
    def text(self):
        return fmt_to_csv(self.scenarios) if (self.out_fmt == "csv") else fmt_to_table(self.scenarios, self.out_fmt)

    def write(self):

        if self.out_dest == "console":
            print(self.text)
            return

        with Path(self.out_dest).open("wb") as fp:
            fp.write(self.text.encode("utf-8"))

    @classmethod
    def write_scenarios(cls, scenarios: List[dict], out_dest, out_fmt):
        ScenariosOutput(scenarios, out_dest, out_fmt).write()
