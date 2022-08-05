"""Tests for day 18 of Advent of Code 2021."""

from day18 import Snailfish, part_a, part_b, snailfish_sum

def test_explode():
    """Test single snailfish number explosion."""
    def assert_explosion(s1: str, s2: str):
        sn1 = Snailfish(s1)
        sn2 = Snailfish(s2)
        did_explode = sn1.explode()
        assert did_explode == True
        assert sn1.data == sn2.data
    assert_explosion("[[[[[9,8],1],2],3],4]",
                     "[[[[0,9],2],3],4]")
    assert_explosion("[7,[6,[5,[4,[3,2]]]]]",
                     "[7,[6,[5,[7,0]]]]")
    assert_explosion("[[6,[5,[4,[3,2]]]],1]",
                     "[[6,[5,[7,0]]],3]")
    assert_explosion("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
                     "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    assert_explosion("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
                     "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")


def test_split():
    """Test single snailfish number split."""
    def assert_split(s1: str, s2: str):
        sn1 = Snailfish(s1)
        sn2 = Snailfish(s2)
        did_split = sn1.split()
        assert did_split
        assert sn1.data == sn2.data
    assert_split("[[[[0,7],4],[15,[0,13]]],[1,1]]",
                 "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
    assert_split("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]",
                 "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")


def test_addition():
    """Test snailfish pair addition and reduction."""
    s1 = "[[[[4,3],4],4],[7,[[8,4],9]]]"
    s2 = "[1,1]"
    s3 = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    sn1 = Snailfish(s1)
    sn2 = Snailfish(s2)
    sn3 = sn1.add(sn2)

    assert sn3.data == Snailfish(s3).data
    
def test_list_sum():
    """Test adding up a list of snailfish numbers."""
    def assert_sum(sum_str: str, list_str: str):
        snlist = [Snailfish(s) for s in list_str.split()]
        assert snailfish_sum(snlist).data == Snailfish(sum_str).data
    sum1 = "[[[[1,1],[2,2]],[3,3]],[4,4]]"
    list1 = """[1,1]
[2,2]
[3,3]
[4,4]"""
    assert_sum(sum1, list1)
    
    sum2 = "[[[[3,0],[5,3]],[4,4]],[5,5]]"

    list2 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""
    assert_sum(sum2, list2)

    sum3 = "[[[[5,0],[7,4]],[5,5]],[6,6]]"

    list3 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""
    assert_sum(sum3, list3)

    sum4 = "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"

    list4 = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
    assert_sum(sum4, list4)

def test_magnitude():
    """Test the magnitude of snailfish numbers."""
    assert Snailfish("[[1,2],[[3,4],5]]").magnitude() == 143.
    assert Snailfish("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]").magnitude() == 1384
    assert Snailfish("[[[[1,1],[2,2]],[3,3]],[4,4]]").magnitude() == 445
    assert Snailfish("[[[[3,0],[5,3]],[4,4]],[5,5]]").magnitude() == 791
    assert Snailfish("[[[[5,0],[7,4]],[5,5]],[6,6]]").magnitude() == 1137
    assert Snailfish("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude() == 3488


# Test data given as a multiline string.
sample_input_data = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""


sample_solution_a = 4140


sample_solution_b = 3993


def test_part_a():
    """Test the solution on sample data for part A."""
    assert part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert part_b(sample_input_data) == sample_solution_b
