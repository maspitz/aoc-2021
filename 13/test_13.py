"""Tests for day 13 of Advent of Code 2021."""

import day13

# Test data given as a multiline string.
sample_input_data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

sample_solution_a = 17

# I store the dots, not the paper, so the square test pattern
# and all other plots will not include empty rows on the bottom
# not empty columns on the right.
# Also, the last row is terminated by a newline.

sample_solution_b = """#####
#   #
#   #
#   #
#####
"""


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day13.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day13.part_b(sample_input_data) == sample_solution_b
