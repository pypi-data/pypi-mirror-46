from itertools import product
from pathlib import Path
from re import findall
from typing import List

from more_itertools import circular_shifts
from tabulate import tabulate

from bets.model.matches import Matches, RANKS, OUTCOMES
from bets.utils import log
from bets.utils.decorators import cachedproperty
from bets.utils.string_utils import fmt_tuple


class Scenario:
    matches: Matches
    outcomes: List[str]
    ratios: List[str]
    ranks: List[str]
    outcome_counts: dict
    ranks_counts: dict
    total_ratio: float
    tuple: tuple

    def __str__(self):
        return str(self.tuple)

    @cachedproperty
    def csv(self):
        return ",".join(fmt_tuple(self.tuple).split())

    @cachedproperty
    def values(self):
        return fmt_tuple(self.tuple).split()

    @cachedproperty
    def columns(self) -> List[str]:
        columns = []
        for i in range(len(self.outcomes)):
            columns.append(f"O-{i + 1}")
        for i in range(len(self.ratios)):
            columns.append(f"R-{i + 1}")
        for i in range(len(self.ranks)):
            columns.append(f"[O-{i + 1}]")
        for r in RANKS:
            columns.append(f"n-{r}")
        for o in OUTCOMES:
            columns.append(f"n-{o}")

        columns.append("Total")

        return columns

    @classmethod
    def from_outcomes(cls, outcomes, matches: Matches):
        s = Scenario()
        s.outcomes = outcomes
        s.ratios = tuple(match.outcome2ratio[outcome] for match, outcome in zip(matches, outcomes))
        s.ranks = tuple(match.outcome2rank[outcome] for match, outcome in zip(matches, outcomes))

        s.outcome_counts = {"1": 0, "X": 0, "2": 0}
        for outcome in outcomes:
            s.outcome_counts[outcome] = s.outcome_counts[outcome] + 1

        s.ranks_counts = dict(min=0, med=0, max=0)
        for rank in s.ranks:
            for key in s.ranks_counts.keys():
                if key in rank:
                    s.ranks_counts[key] = s.ranks_counts[key] + 1

        s.total_ratio = 1
        for ratio in s.ratios:
            s.total_ratio = s.total_ratio * ratio
        s.total_ratio = float(s.total_ratio.__format__(".2f"))

        s.tuple = (s.outcomes
                   + tuple(s.ratios)
                   + tuple(s.ranks)
                   + tuple(s.ranks_counts.values())
                   + tuple(s.outcome_counts.values())
                   + (s.total_ratio,))
        return s


class Scenarios:
    def __init__(self, matches: Matches, scenarios: List[Scenario]):
        self.matches = matches
        self.scenarios = scenarios

    def __iter__(self):
        return self.scenarios.__iter__()

    def __str__(self):
        return self.csv

    def __len__(self):
        return len(self.scenarios)

    def __delitem__(self, key):
        if isinstance(key, int):
            del self.scenarios[key]
        elif isinstance(key, Scenario):
            if key in self.scenarios:
                idx = self.scenarios.index(key)
                del self.scenarios[idx]

    def copy(self):
        return Scenarios(self.matches, self.scenarios.copy())

    @classmethod
    def from_matches(cls, matches: Matches):
        scenarios = [Scenario.from_outcomes(outcomes, matches)
                     for outcomes
                     in product(OUTCOMES, repeat=len(matches))]
        return cls(matches, scenarios)

    @cachedproperty
    def columns(self) -> List[str]:
        return self.scenarios[0].columns

    @property
    def csv(self) -> str:
        headers = ",".join(self.columns)
        data = "\n".join(s.csv for s in self.scenarios)
        return f"{headers}\n{data}"

    @property
    def table(self) -> str:
        return tabulate(
            tabular_data=[s.tuple for s in self.scenarios],
            headers=["ID"] + self.columns,
            tablefmt="fancy_grid",
            stralign="center",
            floatfmt=".2f",
            numalign="decimal",
            showindex=True
        )

    def filter(self, filter_func):
        return Scenarios(self.matches, list(filter(filter_func, self.scenarios)))

    def filter_by_total_occurrences(self, value, min_count, max_count):
        def is_matching_counts(scenario: Scenario):
            count = 0
            values = scenario.ranks if (value in RANKS) else scenario.outcomes
            for v in values:
                if value in v:
                    count = count + 1
            return min_count <= count <= max_count

        return self.filter(is_matching_counts)

    def filter_by_sequential_occurrences(self, value, max_count):
        def is_matching_count(scenario: Scenario):
            values = scenario.outcomes if (value in OUTCOMES) else scenario.ranks
            for shift in circular_shifts(values):
                if value in OUTCOMES:
                    matching_parts = findall(f"[{value}]+", "".join(shift))
                else:
                    matching_parts = findall(f"/?((?:{value})+)", "".join(shift))

                if matching_parts:
                    for part in matching_parts:
                        actual_count = len(part) if (value in OUTCOMES) else (len(part) // 3)
                        if actual_count > max_count:
                            return False
            return True

        return self.filter(is_matching_count)

    def write_to_csv(self, file):
        Path(file).write_text(self.csv, encoding="utf-8")

    def write_to_txt(self, file):
        Path(file).write_text(self.table, encoding="utf-8")

    def write_to_file(self, file: str):
        suffix = file[file.rfind(".") + 1:].lower()
        write_func = self.write_to_csv if suffix == "csv" else self.write_to_txt
        write_func(file)


def main():
    matches = Matches.random(3)
    scenarios = Scenarios.from_matches(matches)
    print(scenarios.table)
    print(scenarios.csv)


if __name__ == '__main__':
    import logging

    log.init(level=logging.INFO)
    main()
