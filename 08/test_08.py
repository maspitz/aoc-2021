"""Tests for day 08 of Advent of Code 2021."""

import day08

# Test data given as a multiline string.

sample_input_data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

sample_solution_a = 26

sample_solution_b = 61229


### simple sample example

simple_sample = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""

simple_sample_patterns = {"acedgfb": 8,
                          "cdfbe": 5,
                          "gcdfa": 2,
                          "fbcad": 3,
                          "dab": 7,
                          "cefabd": 9,
                          "cdfgeb": 6,
                          "eafb": 4,
                          "cagedb": 0,
                          "ab": 1}


def test_simple_parse():
    """Test the parsing of patterns and outputs on the provided simple line."""

    patterns, outputs = day08.get_segments(simple_sample)
    assert patterns == [frozenset(x) for x in simple_sample_patterns.keys()]
    assert outputs == [frozenset(x) for x in ["cdfeb", "fcadb", "cdfeb", "cdbaf"]]

    
def test_simple_decoding_patterns():
    """Test the decoding of patterns of the provided simple line."""

    patterns, outputs = day08.get_segments(simple_sample)

    pd = day08.pattern_dictionary(patterns)
    simple_dict = {frozenset(code_segs): digit
                   for code_segs, digit in simple_sample_patterns.items()}
    assert pd == simple_dict


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day08.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day08.part_b(sample_input_data) == sample_solution_b
