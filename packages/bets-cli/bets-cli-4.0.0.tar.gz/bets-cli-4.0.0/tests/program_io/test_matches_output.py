from tempfile import gettempdir
from time import time
from pathlib import Path
from mock import patch

import pytest

from bets.model.match import Match
from bets.program_io.matches_output import (
    fmt_to_csv,
    fmt_to_table,
    MatchesOutput
)

MATCHES = [
    Match("Man UTD. - Arsenal", 2.78, 3.45, 2.90),
    Match("Liverpool - Barcelona", 2.55, 3.6, 2.75)
]

EXPECTED_CSV = """title,1,X,2,[1],[X],[2],min,med,max,[min],[med],[max]
Man UTD. - Arsenal,2.78,3.45,2.90,min,max,med,2.78,3.45,2.90,1,2,X
Liverpool - Barcelona,2.55,3.60,2.75,min,max,med,2.55,3.60,2.75,1,2,X
"""

EXPECTED_TABLE_FANCY_GRID = """╒═══════════════════════╤══════╤══════╤══════╤═══════╤═══════╤═══════╤═══════╤═══════╤═══════╤═════════╤═════════╤═════════╕
│         title         │    1 │    X │    2 │  [1]  │  [X]  │  [2]  │   min │   med │   max │  [min]  │  [med]  │  [max]  │
╞═══════════════════════╪══════╪══════╪══════╪═══════╪═══════╪═══════╪═══════╪═══════╪═══════╪═════════╪═════════╪═════════╡
│  Man UTD. - Arsenal   │ 2.78 │ 3.45 │ 2.90 │  min  │  max  │  med  │  2.78 │  3.45 │  2.90 │    1    │    2    │    X    │
├───────────────────────┼──────┼──────┼──────┼───────┼───────┼───────┼───────┼───────┼───────┼─────────┼─────────┼─────────┤
│ Liverpool - Barcelona │ 2.55 │ 3.60 │ 2.75 │  min  │  max  │  med  │  2.55 │  3.60 │  2.75 │    1    │    2    │    X    │
╘═══════════════════════╧══════╧══════╧══════╧═══════╧═══════╧═══════╧═══════╧═══════╧═══════╧═════════╧═════════╧═════════╛"""

EXPECTED_TABLE_PLAIN = """        title             1     X     2   [1]    [X]    [2]     min    med    max   [min]    [med]    [max]
 Man UTD. - Arsenal    2.78  3.45  2.90   min    max    med    2.78   3.45   2.90     1        2        X
Liverpool - Barcelona  2.55  3.60  2.75   min    max    med    2.55   3.60   2.75     1        2        X"""


def test_fmt_to_csv():
    assert fmt_to_csv(MATCHES) == EXPECTED_CSV


def test_fmt_to_table_fancy_grid():
    assert fmt_to_table(MATCHES, "fancy_grid") == EXPECTED_TABLE_FANCY_GRID


def test_fmt_to_table_plain():
    assert fmt_to_table(MATCHES, "plain") == EXPECTED_TABLE_PLAIN


def _get_temp_file_no_ext() -> str:
    return str(Path(gettempdir()).joinpath(str(int(time()))))


def test_write_to_file_csv():
    csv_file = _get_temp_file_no_ext() + ".csv"
    MatchesOutput.write_matches(MATCHES, csv_file, "csv")
    actual_csv = Path(csv_file).read_text(encoding="utf-8")
    Path(csv_file).unlink()
    assert actual_csv == EXPECTED_CSV


def test_write_to_file_table_fancy_grid():
    txt_file = _get_temp_file_no_ext() + ".txt"
    MatchesOutput.write_matches(MATCHES, txt_file, "fancy_grid")
    actual_text = Path(txt_file).read_text(encoding="utf-8")
    Path(txt_file).unlink()
    assert actual_text == EXPECTED_TABLE_FANCY_GRID


def test_write_to_file_table_plain():
    txt_file = _get_temp_file_no_ext() + ".txt"
    MatchesOutput.write_matches(MATCHES, txt_file, "plain")
    actual_text = Path(txt_file).read_text(encoding="utf-8")
    Path(txt_file).unlink()
    assert actual_text == EXPECTED_TABLE_PLAIN


def test_cant_output_unknown_format():
    with pytest.raises(ValueError):
        MatchesOutput(MATCHES, out_dest="console", fmt="asc")
    with pytest.raises(ValueError):
        MatchesOutput(MATCHES, out_dest="console", fmt=None)
    with pytest.raises(ValueError):
        MatchesOutput(MATCHES, out_dest="console", fmt=[])
    with pytest.raises(ValueError):
        MatchesOutput(MATCHES, out_dest="console", fmt=object())


@patch("builtins.print")
def test_output_to_console(mock_print):

    MatchesOutput.write_matches(MATCHES, "console", "csv")
    mock_print.assert_called_with(EXPECTED_CSV)

    MatchesOutput.write_matches(MATCHES, "console", "fancy_grid")
    mock_print.assert_called_with(EXPECTED_TABLE_FANCY_GRID)

    MatchesOutput.write_matches(MATCHES, "console", "plain")
    mock_print.assert_called_with(EXPECTED_TABLE_PLAIN)
