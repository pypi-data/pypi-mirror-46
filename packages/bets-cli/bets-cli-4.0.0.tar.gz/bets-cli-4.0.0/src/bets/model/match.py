from bets.utils import log
from bets.utils.num_utils import parse_float


class Match:
    OUTCOMES = ["1", "X", "2"]
    RANKS = ["min", "med", "max"]
    COLUMNS = ["title", "1", "X", "2", "[1]", "[X]", "[2]", "min", "med", "max", "[min]", "[med]", "[max]"]

    def __init__(self, title, ratio_1, ratio_x, ratio_2):
        log.debug("creating Match("
                  "title={title}, "
                  "ratio_1={ratio_1}, "
                  "ratio_x={ratio_x}, "
                  "ratio_2={ratio_2})...".format(title=title, ratio_1=ratio_1, ratio_x=ratio_x, ratio_2=ratio_2))

        self.title = title
        self.ratio_1 = parse_float(ratio_1)
        self.ratio_x = parse_float(ratio_x)
        self.ratio_2 = parse_float(ratio_2)
        self.ratio_min, self.ratio_med, self.ratio_max = sorted((self.ratio_1, self.ratio_x, self.ratio_2))

        self.ratios = {
            "1": self.ratio_1,
            "X": self.ratio_x,
            "2": self.ratio_2,
        }

        self.ranks = {
            "min": self.ratio_min,
            "med": self.ratio_med,
            "max": self.ratio_max,
        }

        self.outcome_ranks = {
            "1": [],
            "X": [],
            "2": []
        }
        self.ranks_outcomes = {
            "min": [],
            "med": [],
            "max": [],
        }

        self.ranks_ratios = {}

        for outcome, outcome_ratio in self.ratios.items():
            for rank, rank_ratio in self.ranks.items():
                if outcome_ratio == rank_ratio:
                    self.outcome_ranks[outcome].append(rank)
                    self.ranks_outcomes[rank].append(outcome)
                    self.ranks_ratios[rank] = rank_ratio

        for outcome, ranks in self.outcome_ranks.items():
            if len(ranks) > 1:
                self.outcome_ranks[outcome] = "/".join(ranks)
            else:
                self.outcome_ranks[outcome] = ranks[0]

        for rank, outcomes in self.ranks_outcomes.items():
            if len(outcomes) > 1:
                self.ranks_outcomes[rank] = "/".join(outcomes)
            else:
                self.ranks_outcomes[rank] = outcomes[0]

        self.tuple = (
                (title,)
                + tuple(self.ratios.values())
                + tuple(self.outcome_ranks.values())
                + tuple(self.ranks_ratios.values())
                + tuple(self.ranks_outcomes.values())
        )

    def __eq__(self, other):
        if not isinstance(other, Match):
            return False
        return (
                self.title == other.title
                and self.ratio_1 == other.ratio_1
                and self.ratio_x == other.ratio_x
                and self.ratio_2 == other.ratio_2
        )

    def __repr__(self):
        return f"Match(\"{self.title}\", {self.ratio_1}, {self.ratio_x}, {self.ratio_2})"
