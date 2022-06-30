"""Tests for day 06 of Advent of Code 2021."""

import day06

# Test data given as a multiline string.
sample_input_data = """3,4,3,1,2"""

sample_solution_a = 5934

sample_solution_b = 26984457539


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day06.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day06.part_b(sample_input_data) == sample_solution_b
