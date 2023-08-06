import json

from pathlib import Path
from typing import List, Union, Iterable, Dict
from itertools import chain

from bets.model.stats.abstract_stats import AbstractStats
from bets.model.stats.outcome_stats import OutcomeStats
from bets.model.stats.ratio_stats import RatioStats
from bets.model.stats.score_stats import ScoreStats
from bets.utils.string_utils import csv_from_dicts


class StatsCollection(AbstractStats):
    KEYS = ["size",
            "n_1", "n_X", "n_2",
            "perc_1", "perc_X", "perc_2",
            "n_min", "n_med", "n_max",
            "perc_min", "perc_med", "perc_max",
            "ratio_total", "ratio_mean", "ratio_geometric_mean",
            "ratio_perc_total_mean", "ratio_perc_total_mean_geometric",
            "outcomes", "ranks", "ratios"]

    def __init__(self, matches: Iterable[Union[OutcomeStats, ScoreStats]] = None):
        self._matches: List[Union[OutcomeStats, ScoreStats]] = list(matches) if matches else []

    def __iter__(self):
        return self._matches.__iter__()

    def __len__(self):
        return len(self._matches)

    def __add__(self, other):
        if isinstance(other, StatsCollection):
            return StatsCollection(chain(self._matches, other._matches))

        raise TypeError(type(other))

    def __bool__(self):
        return bool(self._matches)

    @classmethod
    def read_json(cls, file=None) -> "StatsCollection":
        if file is None:
            file = r"D:\PROJECT_HOME\f_stats\src\f_stats\storage\matches.json"
        path = Path(file)
        matches = []
        with path.open("rb") as fp:
            matches_dicts = json.loads(fp.read().decode("utf-8"))
            for m in matches_dicts:
                matches.append(ScoreStats(m["ratio_1"],
                                          m["ratio_x"],
                                          m["ratio_2"],
                                          m["host_score"],
                                          m["guest_score"],
                                          m["host_team"],
                                          m["guest_team"],
                                          m["date"],
                                          m["country"],
                                          m["tournament"]))
        return StatsCollection(matches)

    @property
    def matches_dicts(self) -> List[Dict[str, Union[int, float, str]]]:
        return [m.as_dict() for m in self]

    @property
    def size(self) -> int:
        return len(self._matches)

    @property
    def n_1(self) -> int:
        return len([m for m in self if m.outcome == "1"])

    @property
    def n_X(self) -> int:
        return len([m for m in self if m.outcome == "X"])

    @property
    def n_2(self) -> int:
        return len([m for m in self if m.outcome == "2"])

    @property
    def perc_1(self) -> float:
        return round(((self.n_1 / len(self)) * 100), 2)

    @property
    def perc_X(self) -> float:
        return round(((self.n_X / len(self)) * 100), 2)

    @property
    def perc_2(self) -> float:
        return round(((self.n_2 / len(self)) * 100), 2)

    @property
    def n_min(self) -> int:
        return len([m for m in self._matches if "min" in m.rank])

    @property
    def n_med(self) -> int:
        return len([m for m in self._matches if "med" in m.rank])

    @property
    def n_max(self) -> int:
        return len([m for m in self._matches if "max" in m.rank])

    @property
    def perc_min(self) -> float:
        return round(((self.n_min / len(self)) * 100), 2)

    @property
    def perc_med(self) -> float:
        return round(((self.n_med / len(self)) * 100), 2)

    @property
    def perc_max(self) -> float:
        return round(((self.n_max / len(self)) * 100), 2)

    @property
    def ratio_total(self) -> float:
        total = 1
        for m in self:
            total *= m.ratio

        return round(total, 2)

    @property
    def ratio_mean(self) -> float:
        mean = 1
        for m in self:
            mean *= m.ratio_mean
        return round(mean, 2)

    @property
    def ratio_geometric_mean(self) -> float:
        mean_geometric = 1
        for m in self:
            mean_geometric *= m.ratio_geometric_mean
        return round(mean_geometric, 2)

    @property
    def ratio_perc_total_mean(self) -> float:
        return round(((self.ratio_total / self.ratio_mean) * 100), 2)

    @property
    def ratio_perc_total_mean_geometric(self) -> float:
        return round(((self.ratio_total / self.ratio_geometric_mean) * 100), 2)

    @property
    def outcomes(self) -> str:
        return " ".join([m.outcome for m in self])

    @property
    def ranks(self) -> str:
        return " ".join([m.rank for m in self])

    @property
    def ratios(self) -> str:
        return " ".join([f"{m.ratio:.02f}" for m in self])

    @property
    def unique_countries(self) -> List[str]:
        return list(sorted(set([m.country for m in self if m.country])))

    @property
    def unique_dates(self) -> List[str]:
        return list(sorted(set(m.date for m in self if m.date)))

    @property
    def unique_ranks(self) -> List[str]:
        return list(sorted(set(self.ranks.split(" "))))

    @property
    def unique_tournaments(self) -> List[str]:
        return list(sorted(set([m.tournament for m in self if m.tournament])))

    @property
    def unique_ratios(self) -> List[float]:
        return [float(value) for value in sorted(set(self.ratios.split(" ")))]

    def get_counters(self) -> Dict[str, int]:
        return {
            "Countries": len(self.unique_countries),
            "Tournaments": len(self.unique_tournaments),
            "Dates": len(self.unique_dates),
            "Records": len(self),
        }

    def append(self, stats: Union[RatioStats, OutcomeStats, ScoreStats]):
        if not isinstance(stats, (RatioStats, OutcomeStats, ScoreStats)):
            raise TypeError(type(stats))

        self._matches.append(stats)

    def get_matches_dicts(self, skip_columns: List[str] = None) -> List[Dict[str, Union[int, float, str]]]:
        result = [m.as_dict() for m in self]
        if skip_columns:
            for item in result:
                for column in skip_columns:
                    if column in item:
                        del item[column]
        return result

    def sort_by_rank(self) -> "StatsCollection":
        self._matches.sort(key=(lambda m: m["rank"]))
        return self

    def sort_by_ratio(self) -> "StatsCollection":
        self._matches.sort(key=(lambda m: m["ratio"]))
        return self

    def sort_by_outcome(self) -> "StatsCollection":
        self._matches.sort(key=(lambda m: m["outcome"]))
        return self

    def with_country(self, country: str) -> "StatsCollection":
        return StatsCollection(m for m in self if m.country == country)

    def with_date(self, date: str) -> "StatsCollection":
        return StatsCollection(m for m in self if m.date == date)

    def with_rank(self, rank: str) -> "StatsCollection":
        return StatsCollection(m for m in self if m.rank == rank)

    def with_ratio(self, ratio: float) -> "StatsCollection":
        return StatsCollection(m for m in self if m.ratio == ratio)

    def with_tournament(self, tournament: str) -> "StatsCollection":
        return StatsCollection(m for m in self if m.tournament == tournament)

    def with_tournament_contains(self, value: str) -> "StatsCollection":
        return StatsCollection(m for m in self if value in m.tournament)

    def with_similar_ratios_to(self, sample: RatioStats) -> "StatsCollection":
        return StatsCollection(m for m in self if m.is_having_similar_ratios_to(sample))

    def with_similar_outcome_ratio_percentages_to(self, sample: RatioStats) -> "StatsCollection":
        return StatsCollection(m for m in self if m.is_having_similar_outcome_ratio_percentages_to(sample))

    def with_similar_rank_ratio_percentages_to(self, sample: RatioStats) -> "StatsCollection":
        return StatsCollection(m for m in self if m.is_having_similar_rank_ratio_percentages_to(sample))

    def by_country(self) -> Dict[str, "StatsCollection"]:
        return {country: self.with_country(country) for country in self.unique_countries}

    def by_date(self) -> Dict[str, "StatsCollection"]:
        return {date: self.with_date(date) for date in self.unique_dates}

    def by_rank(self) -> Dict[str, "StatsCollection"]:
        return {rank: self.with_rank(rank).sort_by_outcome() for rank in self.unique_ranks}

    def by_ratio(self) -> Dict[str, "StatsCollection"]:
        return {ratio: self.with_ratio(ratio).sort_by_outcome() for ratio in self.unique_ratios}

    def tournaments_by_countries(self) -> Dict[str, List[str]]:
        return {country: list(sorted(set([m.country for m in stats if m.country])))
                for country, stats
                in self.by_country().items()}

    def agg_date(self) -> Dict[str, List[Dict[str, Union[int, float, str]]]]:
        return {date: date_stats.get_matches_dicts()
                for date, date_stats
                in self.by_date().items()}

    def agg_rank(self) -> Dict[str, List[Dict[str, Union[int, float, str]]]]:
        return {rank: rank_stats.get_matches_dicts()
                for rank, rank_stats
                in self.by_rank().items()}

    def agg_ratio(self: "StatsCollection") -> Dict[str, List[Dict[str, Union[int, float, str]]]]:
        ratio_stats = self.by_ratio()
        return {f"{ratio:.02f}": ratio_stats[ratio].get_matches_dicts()
                for ratio
                in sorted(ratio_stats.keys(), reverse=True)}

    def summary_by_date(self) -> List[Dict[str, Union[int, float, str]]]:
        stats_by_date = [dict(date=date, **stats.as_dict())
                         for date, stats
                         in self.by_date().items()]
        stats_by_date.sort(key=(lambda s: s["size"]))
        return stats_by_date

    def summary_by_rank(self) -> List[Dict[str, Union[int, float, str]]]:
        stats_by_rank = [dict(rank=rank, **stats.as_dict())
                         for rank, stats
                         in self.by_rank().items()]

        stats_by_rank.sort(key=(lambda s: s["size"]))
        return stats_by_rank

    def summary_by_ratio(self) -> List[Dict[str, Union[int, float, str]]]:
        stats_by_ratio = [dict(ratio=ratio, won="", **stats.as_dict())
                          for ratio, stats
                          in self.by_ratio().items()]

        for item in stats_by_ratio:
            ratio = item["ratio"]
            ratio_occurrences = len([m for m in self if (ratio in m.ratios)])
            size = item["size"]
            item["won"] = f"{size}/{ratio_occurrences}"

        stats_by_ratio.sort(key=(lambda s: (eval(s["won"]), s["size"])))

        return stats_by_ratio

    def to_csv(self, columns: List[str] = None) -> str:
        columns = columns or self._matches[0].KEYS
        dicts = [m.as_dict() for m in self]
        return csv_from_dicts(dicts, columns)
