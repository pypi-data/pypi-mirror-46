import pytest

from bets.utils import num_utils


def test_parse_float_handles_string_integer():
    string_integer = "2"
    assert isinstance(num_utils.parse_float(string_integer), float)
    assert num_utils.parse_float(string_integer) == 2.0


def test_parse_float_handles_string_integer_with_spaces():
    string_integer_with_spaces = "10 000"
    assert isinstance(num_utils.parse_float(string_integer_with_spaces), float)
    assert num_utils.parse_float(string_integer_with_spaces) == 10000.0


def test_parse_float_handles_string_float_with_dot():
    float_with_dot = "3.14"
    assert isinstance(num_utils.parse_float(float_with_dot), float)
    assert num_utils.parse_float(float_with_dot) == 3.14


def test_parse_float_handles_string_float_with_comma():
    float_with_comma = "3,14"
    assert isinstance(num_utils.parse_float(float_with_comma), float)
    assert num_utils.parse_float(float_with_comma) == 3.14


def test_parse_float_handles_string_float_with_thousands_comma():
    float_with_thousands_comma = "2,000.2"
    assert isinstance(num_utils.parse_float(float_with_thousands_comma), float)
    assert num_utils.parse_float(float_with_thousands_comma) == 2000.2


def test_parse_float_handles_string_float_with_thousands_comma_and_spaces():
    float_with_thousands_comma_and_spaces = "3, 000, 000 . 4 "
    assert isinstance(num_utils.parse_float(float_with_thousands_comma_and_spaces), float)
    assert num_utils.parse_float(float_with_thousands_comma_and_spaces) == 3000000.4


def test_parse_float_raises_value_error_when_not_parsed():
    with pytest.raises(ValueError):
        num_utils.parse_float(object())

    with pytest.raises(ValueError):
        num_utils.parse_float("xd,2")


def test_generate_variations_size():
    for variation_size in range(2, 13):
        assert len(list(num_utils.generate_variations(("1", "X", "2"), variation_size))) == 3 ** variation_size


def test_multiply_all():
    assert num_utils.multiply_all((2, 3, 4)) == 24
    assert num_utils.multiply_all([1, 5, 2]) == 10
    assert num_utils.multiply_all([2.5, 10]) == 25
    assert num_utils.multiply_all([2.5, 0]) == 0


def test_generate_variations_with_known_values():
    known_variations = [
        [('1',),
         ('X',),
         ('2',)], [('1', '1'),
                   ('1', 'X'),
                   ('1', '2'),
                   ('X', '1'),
                   ('X', 'X'),
                   ('X', '2'),
                   ('2', '1'),
                   ('2', 'X'),
                   ('2', '2')], [('1', '1', '1'),
                                 ('1', '1', 'X'),
                                 ('1', '1', '2'),
                                 ('1', 'X', '1'),
                                 ('1', 'X', 'X'),
                                 ('1', 'X', '2'),
                                 ('1', '2', '1'),
                                 ('1', '2', 'X'),
                                 ('1', '2', '2'),
                                 ('X', '1', '1'),
                                 ('X', '1', 'X'),
                                 ('X', '1', '2'),
                                 ('X', 'X', '1'),
                                 ('X', 'X', 'X'),
                                 ('X', 'X', '2'),
                                 ('X', '2', '1'),
                                 ('X', '2', 'X'),
                                 ('X', '2', '2'),
                                 ('2', '1', '1'),
                                 ('2', '1', 'X'),
                                 ('2', '1', '2'),
                                 ('2', 'X', '1'),
                                 ('2', 'X', 'X'),
                                 ('2', 'X', '2'),
                                 ('2', '2', '1'),
                                 ('2', '2', 'X'),
                                 ('2', '2', '2')], [('1', '1', '1', '1'),
                                                    ('1', '1', '1', 'X'),
                                                    ('1', '1', '1', '2'),
                                                    ('1', '1', 'X', '1'),
                                                    ('1', '1', 'X', 'X'),
                                                    ('1', '1', 'X', '2'),
                                                    ('1', '1', '2', '1'),
                                                    ('1', '1', '2', 'X'),
                                                    ('1', '1', '2', '2'),
                                                    ('1', 'X', '1', '1'),
                                                    ('1', 'X', '1', 'X'),
                                                    ('1', 'X', '1', '2'),
                                                    ('1', 'X', 'X', '1'),
                                                    ('1', 'X', 'X', 'X'),
                                                    ('1', 'X', 'X', '2'),
                                                    ('1', 'X', '2', '1'),
                                                    ('1', 'X', '2', 'X'),
                                                    ('1', 'X', '2', '2'),
                                                    ('1', '2', '1', '1'),
                                                    ('1', '2', '1', 'X'),
                                                    ('1', '2', '1', '2'),
                                                    ('1', '2', 'X', '1'),
                                                    ('1', '2', 'X', 'X'),
                                                    ('1', '2', 'X', '2'),
                                                    ('1', '2', '2', '1'),
                                                    ('1', '2', '2', 'X'),
                                                    ('1', '2', '2', '2'),
                                                    ('X', '1', '1', '1'),
                                                    ('X', '1', '1', 'X'),
                                                    ('X', '1', '1', '2'),
                                                    ('X', '1', 'X', '1'),
                                                    ('X', '1', 'X', 'X'),
                                                    ('X', '1', 'X', '2'),
                                                    ('X', '1', '2', '1'),
                                                    ('X', '1', '2', 'X'),
                                                    ('X', '1', '2', '2'),
                                                    ('X', 'X', '1', '1'),
                                                    ('X', 'X', '1', 'X'),
                                                    ('X', 'X', '1', '2'),
                                                    ('X', 'X', 'X', '1'),
                                                    ('X', 'X', 'X', 'X'),
                                                    ('X', 'X', 'X', '2'),
                                                    ('X', 'X', '2', '1'),
                                                    ('X', 'X', '2', 'X'),
                                                    ('X', 'X', '2', '2'),
                                                    ('X', '2', '1', '1'),
                                                    ('X', '2', '1', 'X'),
                                                    ('X', '2', '1', '2'),
                                                    ('X', '2', 'X', '1'),
                                                    ('X', '2', 'X', 'X'),
                                                    ('X', '2', 'X', '2'),
                                                    ('X', '2', '2', '1'),
                                                    ('X', '2', '2', 'X'),
                                                    ('X', '2', '2', '2'),
                                                    ('2', '1', '1', '1'),
                                                    ('2', '1', '1', 'X'),
                                                    ('2', '1', '1', '2'),
                                                    ('2', '1', 'X', '1'),
                                                    ('2', '1', 'X', 'X'),
                                                    ('2', '1', 'X', '2'),
                                                    ('2', '1', '2', '1'),
                                                    ('2', '1', '2', 'X'),
                                                    ('2', '1', '2', '2'),
                                                    ('2', 'X', '1', '1'),
                                                    ('2', 'X', '1', 'X'),
                                                    ('2', 'X', '1', '2'),
                                                    ('2', 'X', 'X', '1'),
                                                    ('2', 'X', 'X', 'X'),
                                                    ('2', 'X', 'X', '2'),
                                                    ('2', 'X', '2', '1'),
                                                    ('2', 'X', '2', 'X'),
                                                    ('2', 'X', '2', '2'),
                                                    ('2', '2', '1', '1'),
                                                    ('2', '2', '1', 'X'),
                                                    ('2', '2', '1', '2'),
                                                    ('2', '2', 'X', '1'),
                                                    ('2', '2', 'X', 'X'),
                                                    ('2', '2', 'X', '2'),
                                                    ('2', '2', '2', '1'),
                                                    ('2', '2', '2', 'X'),
                                                    ('2', '2', '2', '2')]
    ]

    for variation_size in range(1, 5):
        expected_variations = known_variations[variation_size - 1]
        current_variation_index = 0
        for actual_variation in num_utils.generate_variations(("1", "X", "2"), variation_size):
            assert expected_variations[current_variation_index] == actual_variation
            current_variation_index += 1
