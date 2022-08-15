"""Tests for day 21 of Advent of Code 2021."""

import day21

# Test data given as a multiline string.
sample_input_data = """Player 1 starting position: 4
Player 2 starting position: 8"""

sample_solution_a = 739785

sample_solution_b = 444356092776315


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day21.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day21.part_b(sample_input_data) == sample_solution_b
