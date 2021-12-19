import pytest
from solver import (
    tokenize,
    parse,
    solve1,
    solve2,
    find_exploding_pair,
    explode_pair_at,
    reduce_snailnum,
    sum_snailnums,
    to_string,
)

TESTDATA = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here

def test_explode():

    def explode(s):
        tokens = tokenize(s)
        pos = find_exploding_pair(tokens)
        explode_pair_at(tokens, pos)
        return to_string(tokens)

    assert explode("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"
    assert explode("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
    assert explode("[[6,[5,[4,[3,2]]]],1]") == "[[6,[5,[7,0]]],3]"
    assert explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    assert explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"


def test_reduce():

    def reduce(s):
        tokens = tokenize(s)
        reduce_snailnum(tokens)
        return to_string(tokens)

    assert reduce("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


def test_sum():

    def sum(s):
        return to_string(sum_snailnums(parse(s)))

    assert sum("""[1,1]
[2,2]
[3,3]
[4,4]""") == "[[[[1,1],[2,2]],[3,3]],[4,4]]"
    assert sum("""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]""") == "[[[[3,0],[5,3]],[4,4]],[5,5]]"
    assert sum("""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]""") == "[[[[5,0],[7,4]],[5,5]],[6,6]]"
    assert sum("""[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""") == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"


def test_solve1(parsed_data):
    assert solve1(parsed_data) == 4140


def test_solve2(parsed_data):
    assert solve2(parsed_data) == 3993
