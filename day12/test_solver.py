import pytest
from solver import parse, solve1, solve2

TESTDATA = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 10


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 36
