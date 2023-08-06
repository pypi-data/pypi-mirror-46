import logging
from typing import List

from bets.model.match import Match

from bets.utils.num_utils import (
    multiply_all,
    generate_variations
)

_log = logging.getLogger(__name__)

ALL_RANKS = "min med max min/med min/max med/max".split(" ")
ALL_OUTCOMES = "1 X 2 1/X 1/2 X/2".split(" ")


class ScenariosGenerator:

    def __init__(self, matches: List[Match]):
        _log.debug("created ScenariosGenerator for [{}] matches!".format(len(matches)))
        self.matches = matches.copy()
        self.outcomes = list(generate_variations(("1", "X", "2"), len(matches)))
        self.scenarios_outcomes = self._generate_scenarios_outcomes()
        self.ranks = list(self._generate_ranks())
        self.ratios = list(self._generate_ratios())
        self.ranks_counts = list(self._generate_ranks_counts())
        self.outcomes_counts = list(self._generate_outcomes_counts())
        self.total_ratios = list(self._generate_total_ratios())

    def _generate_scenarios_outcomes(self):
        for scenario_outcomes in self.outcomes:
            yield {f"o-{i}": outcome
                   for i, outcome
                   in enumerate(scenario_outcomes)}

    def _generate_ranks(self):
        for scenario_outcomes in self.outcomes:
            yield {f"rnk-{i}": match.outcome_ranks[outcome]
                   for i, (match, outcome) in
                   enumerate(zip(self.matches, scenario_outcomes))}

    def _generate_ratios(self):
        for scenario_outcomes in self.outcomes:
            yield {f"r-{i}": match.ratios[outcome]
                   for i, (match, outcome)
                   in enumerate(zip(self.matches, scenario_outcomes))}

    def _generate_ranks_counts(self):
        for scenario_ranks in self.ranks:
            yield {f"n-{rank}": list(scenario_ranks.values()).count(rank)
                   for rank
                   in ALL_RANKS}

    def _generate_outcomes_counts(self):
        for scenario_outcomes in self.outcomes:
            yield {f"n-{outcome}": scenario_outcomes.count(outcome)
                   for outcome
                   in ALL_OUTCOMES}

    def _generate_total_ratios(self):
        for scenario_ratios in self.ratios:
            yield {"total_ratio": multiply_all(scenario_ratios.values())}

    def generate_scenarios(self):
        for (total_ratio,
             outcomes,
             ranks,
             ratios,
             rank_counts,
             outcome_counts) in zip(self.total_ratios,
                                    self.scenarios_outcomes,
                                    self.ranks,
                                    self.ratios,
                                    self.ranks_counts,
                                    self.outcomes_counts):
            yield {**total_ratio, **outcomes, **ranks, **ratios, **rank_counts, **outcome_counts}
