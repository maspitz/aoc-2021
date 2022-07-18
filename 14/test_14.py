"""Tests for day 14 of Advent of Code 2021."""

import day14

# Test data given as a multiline string.
sample_input_data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

sample_solution_a = 1588

sample_solution_b = 2188189693529


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day14.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day14.part_b(sample_input_data) == sample_solution_b
