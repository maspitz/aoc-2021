"""Tests for day 05 of Advent of Code 2021."""

import day05

# Test data given as a multiline string.
sample_input_data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

sample_solution_a = 5

sample_solution_b = 12


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day05.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day05.part_b(sample_input_data) == sample_solution_b
