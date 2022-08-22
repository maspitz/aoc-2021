"""Tests for day 23 of Advent of Code 2021."""

import day23

# Test data given as a multiline string.
sample_input_data = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

sample_solution_a = 12521

sample_solution_b = 44169


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day23.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day23.part_b(sample_input_data) == sample_solution_b
