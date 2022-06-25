"""Tests for day 03 of Advent of Code 2021."""

import day03

# Test data given as a multiline string.
sample_input_data = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

sample_solution_a = 198

sample_solution_b = 230


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day03.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day03.part_b(sample_input_data) == sample_solution_b
