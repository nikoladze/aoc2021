import pytest
from solver import parse, solve1, solve2, run

TESTDATA = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""


@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


def test_binary_convert(parsed_data):
    res = run(parsed_data, [27])
    assert res["z"] == 1
    assert res["y"] == 1
    assert res["x"] == 0
    assert res["w"] == 1
