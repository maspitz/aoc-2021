"""Tests for day 25 of Advent of Code 2021."""

import day25

# Test data given as a multiline string.
sample_input_data = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

sample_solution_a = 58


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day25.part_a(sample_input_data) == sample_solution_a


