from bets.model.match import Match


def test_create_match_with_string_ratios():
    title = "Man utd. - Arsenal"
    ratio_1 = "1.2"
    ratio_x = "2,2"
    ratio_2 = " 1.83"

    _match = Match(title, ratio_1, ratio_x, ratio_2)
    assert _match.title == title
    assert _match.ratio_1 == 1.2
    assert _match.ratio_x == 2.2
    assert _match.ratio_2 == 1.83


def test_get_outcome_ratios():
    _match = Match("Barcelona - Liverpool", 2.34, 3.40, 2.5)
    assert tuple(_match.ratios.values()) == (2.34, 3.40, 2.5)


def test_match_eq():
    _match = Match("Barcelona - Liverpool", 2.34, 3.40, 2.5)
    _match2 = Match("Barcelona - Liverpool", 2.34, 3.40, 2.5)
    assert _match == _match
    assert _match == _match2
    assert not _match == None
    assert not _match == 0
    assert not _match == []


def test_ranks_outcomes():
    _match = Match("Barcelona - Liverpool", 2.34, 3.40, 2.5)
    for rank, outcomes in _match.ranks_outcomes.items():
        assert rank in {"min", "med", "max"}
        for o in outcomes.split("/"):
            assert o in "1X2"


def test_get_ranks_outcomes():
    _match = Match("Barcelona - Liverpool", 2.34, 3.40, 2.5)
    expected_outcomes = tuple("1 2 X".split(" "))
    actual_outcomes = tuple(_match.ranks_outcomes.values())
    assert actual_outcomes == expected_outcomes

    _match2 = Match("Man utd. - Arsenal", 2.5, 3.9, 2.5)
    expected_outcomes2 = tuple("1/2 1/2 X".split(" "))
    actual_outcomes2 = tuple(_match2.ranks_outcomes.values())
    assert actual_outcomes2 == expected_outcomes2

    _match3 = Match("Man utd. - Arsenal", 2.5, 2.9, 2.9)
    expected_outcomes3 = tuple("1 X/2 X/2".split(" "))
    actual_outcomes3 = tuple(_match3.ranks_outcomes.values())
    assert actual_outcomes3 == expected_outcomes3


def test_get_outcome_ranks():
    _match = Match("Barcelona - Liverpool", 2.34, 3.40, 2.5)
    expected_outcomes = tuple("min max med".split(" "))
    actual_outcomes = tuple(_match.outcome_ranks.values())
    assert actual_outcomes == expected_outcomes

    _match2 = Match("Man utd. - Arsenal", 2.5, 3.9, 2.5)
    expected_outcomes2 = tuple("min/med max min/med".split(" "))
    actual_outcomes2 = tuple(_match2.outcome_ranks.values())
    assert actual_outcomes2 == expected_outcomes2

    _match3 = Match("Man utd. - Arsenal", 2.5, 2.9, 2.9)
    expected_outcomes3 = tuple("min med/max med/max".split(" "))
    actual_outcomes3 = tuple(_match3.outcome_ranks.values())
    assert actual_outcomes3 == expected_outcomes3
