"""Tests for day 07 of Advent of Code 2021."""

import day07

# Test data given as a multiline string.
sample_input_data = """16,1,2,0,4,2,7,1,2,14"""

sample_solution_a = 37

sample_solution_b = 168


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day07.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day07.part_b(sample_input_data) == sample_solution_b
