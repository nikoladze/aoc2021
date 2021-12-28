import pytest
from solver import parse, solve1, solve2, updated
import numpy as np

TESTDATA = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here

def test_updates(parsed_data):
    new_grid = updated(parsed_data)
    assert (
        new_grid
        == np.array(
            parse(
                "....>.>v.>"
                ".v>.>v.v.v"
                ">v>>..>v.."
                ">>v>v>.>.v"
                ".>v.v...v."
                ">>.>vvv..v"
                "..v...>>.."
                "v...>>vv.v"
                ">.v.v..v.v"
            )
        )
    ).all()

def test_solve1(parsed_data):
    assert solve1(parsed_data) == 58
