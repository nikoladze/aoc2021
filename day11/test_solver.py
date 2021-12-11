import pytest
from solver import parse, solve1, solve2

TESTDATA = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data, 10)
    assert solution == 204


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 195
