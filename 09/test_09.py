"""Tests for day 09 of Advent of Code 2021."""

import day09

# Test data given as a multiline string.
sample_input_data = """2199943210
3987894921
9856789892
8767896789
9899965678"""

sample_solution_a = 15

sample_solution_b = 1134

def test_heightmap_init():
    """Test the Heightmap constructor."""
    hm = day09.Heightmap(sample_input_data)
    assert hm.rows == 5
    assert hm.cols == 10
    assert hm.heights[0,0] == 2
    assert hm.heights[4,9] == 8
    assert hm.heights[2,3] == 6


def test_in_bounds():
    """Test the Heightmap.in_bounds methods."""
    hm = day09.Heightmap(sample_input_data)
    inside =  [(0,0), (0,1), (1,0), (1,1),
               (4,9), (4,8), (3,9), (4,8)]
    outside = [(-1,0), (0,-1), (-1,-1), (-1,1), (1,-1),
               (5,0), (0,10), (5,10), (5,9)]
    for in_bounds_method in [hm.in_bounds, hm.in_bounds_alt]:
        for x in inside:
            assert in_bounds_method(x) == True
        for x in outside:
            assert in_bounds_method(x) == False


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day09.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day09.part_b(sample_input_data) == sample_solution_b
