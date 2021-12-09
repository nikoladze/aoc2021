import pytest
from solver import parse, solve1, solve2

TESTDATA = """2199943210
3987894921
9856789892
8767896789
9899965678"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 15


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 1134
