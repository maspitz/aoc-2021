"""Tests for day 10 of Advent of Code 2021."""

import day10

# Test data given as a multiline string.
sample_input_data = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

sample_solution_a = 26397

sample_solution_b = 288957


def test_part_a():
    """Test the solution on sample data for part A."""
    assert day10.part_a(sample_input_data) == sample_solution_a


def test_part_b():
    """Test the solution on sample data for part B."""
    assert day10.part_b(sample_input_data) == sample_solution_b
