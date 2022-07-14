"""Tests for day 12 of Advent of Code 2021."""

import day12

# Test data given as a multiline string.
sample_input_data_1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

sample_input_data_2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

sample_input_data_3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

sample_solution_a_1 = 10
sample_solution_a_2 = 19
sample_solution_a_3 = 226

sample_solution_b_1 = 36
sample_solution_b_2 = 103
sample_solution_b_3 = 3509


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day12.part_a(sample_input_data_1) == sample_solution_a_1
    assert day12.part_a(sample_input_data_2) == sample_solution_a_2
    assert day12.part_a(sample_input_data_3) == sample_solution_a_3


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day12.part_b(sample_input_data_1) == sample_solution_b_1
    assert day12.part_b(sample_input_data_1) == sample_solution_b_1
    assert day12.part_b(sample_input_data_1) == sample_solution_b_1
