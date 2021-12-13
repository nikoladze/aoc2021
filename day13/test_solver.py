import pytest
from solver import parse, solve1, solve2

TESTDATA = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    coords, instructions = data
    assert coords == [
        [6, 10],
        [0, 14],
        [9, 10],
        [0, 3],
        [10, 4],
        [4, 11],
        [6, 0],
        [6, 12],
        [4, 1],
        [0, 13],
        [10, 12],
        [3, 4],
        [3, 0],
        [8, 4],
        [1, 10],
        [2, 14],
        [8, 10],
        [9, 0],
    ]
    assert instructions == [
        ("y", 7),
        ("x", 5),
    ]


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 17


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    # asserts go here
