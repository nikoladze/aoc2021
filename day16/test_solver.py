import pytest
from solver import parse, solve1, solve2

TESTDATA = """D2FE28"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    assert data == "110100101111111000101000"


# PART 1
def test_solve1(parsed_data):
    assert solve1(parse("8A004A801A8002F478")) == 16
    assert solve1(parse("620080001611562C8802118E34")) == 12
    assert solve1(parse("C0015000016115A2E0802F182340")) == 23
    assert solve1(parse("A0016C880162017C3686B18A3D4780")) == 31


# PART 2
def test_solve2(parsed_data):
    assert solve2(parse("C200B40A82")) == 3
    assert solve2(parse("04005AC33890")) == 54
    assert solve2(parse("880086C3E88112")) == 7
    assert solve2(parse("CE00C43D881120")) == 9
    assert solve2(parse("D8005AC2A8F0")) == 1
    assert solve2(parse("F600BC2D8F")) == 0
    assert solve2(parse("9C005AC2F8F0")) == 0
    assert solve2(parse("9C0141080250320F1802104A08")) == 1
