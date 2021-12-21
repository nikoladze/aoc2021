import pytest
from solver import parse, solve1, solve2

TESTDATA = """Player 1 starting position: 4
Player 2 starting position: 8"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 739785


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 444356092776315
