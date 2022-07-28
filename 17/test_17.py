"""Tests for day 17 of Advent of Code 2021."""

import day17

# Test data given as a multiline string.
sample_input_data = """target area: x=20..30, y=-10..-5"""

sample_solution_a = 45

sample_solution_b = 112


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day17.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day17.part_b(sample_input_data) == sample_solution_b
