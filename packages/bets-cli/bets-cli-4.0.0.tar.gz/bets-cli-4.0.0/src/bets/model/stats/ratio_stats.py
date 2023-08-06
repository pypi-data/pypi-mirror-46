from bets.model.stats.constants import RANKS, OUTCOMES
from bets.model.stats.abstract_stats import AbstractStats


class RatioStats(AbstractStats):
    KEYS = ["date", "country", "tournament", "host_team", "guest_team",
            "ratio_1", "ratio_X", "ratio_2",
            "rank_1", "rank_X", "rank_2",
            "ratio_min", "ratio_med", "ratio_max",
            "outcome_min", "outcome_med", "outcome_max",
            "ratio_perc_1_X", "ratio_perc_X_2", "ratio_perc_1_2",
            "ratio_perc_min_med", "ratio_perc_med_max", "ratio_perc_min_max",
            "ratio_mean", "ratio_geometric_mean", "ratio_perc_mean_geometric_mean"]

    def __init__(self, ratio_1, ratio_X, ratio_2, host_team="", guest_team="", date="", country="", tournament=""):

        self.host_team = host_team
        self.guest_team = guest_team
        self.date = date
        self.country = country
        self.tournament = tournament

        self.ratio_1 = round(float(ratio_1), 2)
        self.ratio_X = round(float(ratio_X), 2)
        self.ratio_2 = round(float(ratio_2), 2)

        self.ratios = (self.ratio_1, self.ratio_X, self.ratio_2)
        self.ratios_sorted = tuple(sorted(self.ratios))

        self.ratio_min = self.ratios_sorted[0]
        self.ratio_med = self.ratios_sorted[1]
        self.ratio_max = self.ratios_sorted[2]

        outcomes_by_rank = {rank: [] for rank in RANKS}
        ranks_by_outcome = {outcome: [] for outcome in OUTCOMES}

        for outcome in OUTCOMES:
            for rank in RANKS:
                if self[f"ratio_{outcome}"] == self[f"ratio_{rank}"]:
                    outcomes_by_rank[rank].append(outcome)
                    ranks_by_outcome[outcome].append(rank)

        self.rank_1 = "/".join(ranks_by_outcome["1"])
        self.rank_X = "/".join(ranks_by_outcome["X"])
        self.rank_2 = "/".join(ranks_by_outcome["2"])

        self.outcome_min = "/".join(outcomes_by_rank["min"])
        self.outcome_med = "/".join(outcomes_by_rank["med"])
        self.outcome_max = "/".join(outcomes_by_rank["max"])

        self.ratio_perc_1_X = round(((self.ratio_1 / self.ratio_X) * 100), 2)
        self.ratio_perc_X_2 = round(((self.ratio_X / self.ratio_2) * 100), 2)
        self.ratio_perc_1_2 = round(((self.ratio_1 / self.ratio_2) * 100), 2)

        self.ratio_perc_min_med = round(((self.ratio_min / self.ratio_med) * 100), 2)
        self.ratio_perc_med_max = round(((self.ratio_med / self.ratio_max) * 100), 2)
        self.ratio_perc_min_max = round(((self.ratio_min / self.ratio_max) * 100), 2)

        self.ratio_mean = round(((self.ratio_1 + self.ratio_X + self.ratio_2) / 3), 2)
        self.ratio_geometric_mean = round(((self.ratio_1 * self.ratio_X * self.ratio_2) ** (1 / 3)), 2)
        self.ratio_perc_mean_geometric_mean = round(((self.ratio_mean / self.ratio_geometric_mean) * 100), 2)

    def is_having_similar_ratios_to(self, other: "RatioStats", delta=0.05) -> bool:
        if isinstance(other, RatioStats):
            if abs(self.ratio_1 - other.ratio_1) <= delta:
                if abs(self.ratio_X - other.ratio_X) <= delta:
                    if abs(self.ratio_2 - other.ratio_2) <= delta:
                        return True
        return False

    def is_having_similar_outcome_ratio_percentages_to(self, other: "RatioStats", delta=0.05) -> bool:
        if isinstance(other, RatioStats):
            if abs(self.ratio_perc_1_X - other.ratio_perc_1_X):
                if abs(self.ratio_perc_X_2 - other.ratio_perc_X_2) <= delta:
                    if abs(self.ratio_perc_1_2 - other.ratio_perc_1_2) <= delta:
                        return True
        return False

    def is_having_similar_rank_ratio_percentages_to(self, other: "RatioStats", delta=0.05) -> bool:
        if isinstance(other, RatioStats):
            if abs(self.ratio_perc_min_med - other.ratio_perc_min_med) <= delta:
                if abs(self.ratio_perc_med_max - other.ratio_perc_med_max) <= delta:
                    if abs(self.ratio_perc_min_max - other.ratio_perc_min_max) <= delta:
                        return True
        return False
