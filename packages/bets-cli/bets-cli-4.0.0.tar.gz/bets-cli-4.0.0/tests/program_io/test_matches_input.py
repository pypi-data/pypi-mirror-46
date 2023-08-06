import logging
import tempfile
from os import path, unlink

import pytest

from bets.model.match import Match

from bets.program_io.matches_input import (
    EfbetParser,
    LinesParser,
    MatchesInput,
)

_log = logging.getLogger(__name__)


def test_parse_line_accepts_only_string():
    with pytest.raises(TypeError):
        LinesParser.parse_line(None)

    with pytest.raises(TypeError):
        LinesParser.parse_line([])

    with pytest.raises(TypeError):
        LinesParser.parse_line(object())

    with pytest.raises(TypeError):
        LinesParser.parse_line(1)


def test_parse_line_raises_value_error_on_empty_string():
    with pytest.raises(ValueError):
        LinesParser.parse_line("")


def test_parse_line_raises_value_error_on_line_with_less_than_4_parts():
    with pytest.raises(ValueError):
        LinesParser.parse_line("1 2 3")


def test_create_match_from_text_line():
    text_line = "Barcelona - Liverpool 2.34 3.40 2.5"
    _match = LinesParser.parse_line(text_line)
    assert _match.title == "Barcelona - Liverpool"
    assert _match.ratio_1 == 2.34
    assert _match.ratio_x == 3.40
    assert _match.ratio_2 == 2.50


def test_parse_text_returns_list_of_single_match_when_one():
    text = """

    Barcelona - Liverpool 2.34 3.40 2.5
    2134
    
    not a match pal
    """

    _matches = LinesParser.parse_text(text)
    assert isinstance(_matches, list)
    assert len(_matches) == 1

    _match = _matches[0]
    assert _match.title == "Barcelona - Liverpool"
    assert _match.ratio_1 == 2.34
    assert _match.ratio_x == 3.40
    assert _match.ratio_2 == 2.50


def test_parse_text_returns_list_of_matches_when_many():
    text = """
    
    Barcelona - Liverpool 2.34 3.40 2.5
    2134
    Man utd. - Arsenal 2.78 3.9 3.5
    123
    """

    _matches = LinesParser.parse_text(text)
    assert isinstance(_matches, list)
    assert len(_matches) == 2

    for _match in _matches:
        assert isinstance(_match, Match)

    assert _matches[0].title == "Barcelona - Liverpool"
    assert _matches[0].ratio_1 == 2.34
    assert _matches[0].ratio_x == 3.40
    assert _matches[0].ratio_2 == 2.5
    assert _matches[1].title == "Man utd. - Arsenal"
    assert _matches[1].ratio_1 == 2.78
    assert _matches[1].ratio_x == 3.90
    assert _matches[1].ratio_2 == 3.50


def test_parse_text_raises_value_error_if_no_matches_in_text():
    with pytest.raises(ValueError):
        LinesParser.parse_text("")

    with pytest.raises(ValueError):
        LinesParser.parse_text("""
        no
        matches here
        pal
        """)
    with pytest.raises(ValueError):
        LinesParser.parse_text("""
        no matches here too
        """)


def test_parse_file_raises_value_error_if_file_path_empty_string():
    with pytest.raises(ValueError):
        MatchesInput("", "lines")


def test_parse_file_returns_list_of_matches_when_in_file():
    text = """
        Barcelona - Liverpool 2.34 3.40 2.5
        2134
        Man utd. - Arsenal 2.78 3.9 3.5
        123
        """

    file_path = path.join(tempfile.gettempdir(), "matches.txt")

    with open(file_path, "wb") as fp:
        fp.write(text.encode("utf-8"))

    _matches = MatchesInput.read_file(file_path)

    unlink(file_path)

    assert isinstance(_matches, list)
    assert len(_matches) == 2

    for _match in _matches:
        assert isinstance(_match, Match)

    assert _matches[0].title == "Barcelona - Liverpool"
    assert _matches[0].ratio_1 == 2.34
    assert _matches[0].ratio_x == 3.40
    assert _matches[0].ratio_2 == 2.5
    assert _matches[1].title == "Man utd. - Arsenal"
    assert _matches[1].ratio_1 == 2.78
    assert _matches[1].ratio_x == 3.90
    assert _matches[1].ratio_2 == 3.50


def test_parse_efbet_paste():
    text = """
            Ел Ехидо 2012 vs Атлетико Санлукуено
            2.70
            2.90
            2.85
            +15 >
            * 22мин.	
            Изара vs КД Виктория
            2.15
            3.00
            3.85
            +15 >
            * 22мин.	
            Мирандес vs SCD Durango
            1.30
            5.25
            11.00
            +15 >
            """

    expected_matches = [Match("Ел Ехидо 2012 vs Атлетико Санлукуено", 2.7, 2.9, 2.85),
                        Match("Изара vs КД Виктория", 2.15, 3.0, 3.85),
                        Match("Мирандес vs SCD Durango", 1.3, 5.25, 11.0)]

    _matches = EfbetParser.parse_text(text)

    for _ in _matches:
        print(_)

    assert expected_matches == _matches

    with pytest.raises(ValueError):
        EfbetParser.parse_text("""Ел Ехидо 2012 vs Атлетико Санлукуено
                                2.70
                                2.90
                                2.85
                                +15 >
                                * 22мин.	""")
