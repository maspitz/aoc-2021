"""Tests for day 15 of Advent of Code 2021."""

import day15

# Test data given as a multiline string.
sample_input_data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

sample_solution_a = 40

sample_solution_b = 315


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day15.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day15.part_b(sample_input_data) == sample_solution_b
