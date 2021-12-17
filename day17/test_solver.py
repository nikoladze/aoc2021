import pytest
from solver import parse, solve1, solve2

TESTDATA = """target area: x=20..30, y=-10..-5"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    assert data == ((20, 30), (-10, -5))


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    # asserts go here


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 112
