from bets.model.stats.outcome_stats import OutcomeStats


class ScoreStats(OutcomeStats):
    KEYS = OutcomeStats.KEYS + ["host_score", "guest_score", "goals_diff"]

    host_score: int
    guest_score: int
    goals_diff: int

    def __init__(self, ratio_1, ratio_X, ratio_2, host_score, guest_score,
                 host_team="", guest_team="", date="", country="", tournament=""):
        host_score = int(host_score)
        guest_score = int(guest_score)
        outcome = ("1" if (host_score > guest_score) else ("2" if guest_score > host_score else "X"))
        super().__init__(ratio_1, ratio_X, ratio_2, outcome, host_team, guest_team, date, country, tournament)

        self.host_score = host_score
        self.guest_score = guest_score
        self.goals_diff = abs(host_score - guest_score)
