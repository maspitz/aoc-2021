"""Tests for day 11 of Advent of Code 2021."""

import day11

# Test data given as a multiline string.
sample_input_data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

sample_solution_a = 1656

sample_solution_b = 195


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day11.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day11.part_b(sample_input_data) == sample_solution_b
