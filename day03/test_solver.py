import pytest
from solver import parse, solve1, solve2

TESTDATA = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 198


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 230
