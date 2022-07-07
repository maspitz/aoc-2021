"""Solves day 10, Advent of Code 2021."""

from aocd.models import Puzzle


DELIMITER_PAIR = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'}


CORRUPTION_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137}


AUTOCOMPLETION_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4}


def syntax_score(input_line: str) -> (str, int):
    """Yields a tuple containing error string and score.

    Error string is either "corrupt" or "incomplete".

    The corruption score is 0 for lines that aren't corrupt.
    The autocompletion score is 0 for lines that are corrupt."""

    expected_closing_stack = []
    
    for delim in input_line:
        if delim in DELIMITER_PAIR:
            # got opening delim: add its closing match to the stack
            expected_closing_stack.append(DELIMITER_PAIR[delim])
        else:
            # got closing delim: compare it to what's on the stack
            expected_delim = expected_closing_stack.pop()
            if delim != expected_delim:
                return "corrupt", CORRUPTION_SCORE[delim]

    incomplete_score = 0
    while expected_closing_stack:
        delim = expected_closing_stack.pop()
        incomplete_score *= 5
        incomplete_score += AUTOCOMPLETION_SCORE[delim]
    return "incomplete", incomplete_score


def autocompletion_score(input_line: str) -> int:
    """Returns the autocompletion score for a line."""


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    score_info = [syntax_score(line) for line in input_data.split('\n')]
    corrupt_scores = [score for err, score in score_info
                      if err == "corrupt"]
    return sum(corrupt_scores)


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    score_info = [syntax_score(line) for line in input_data.split('\n')]
    incomplete_scores = [score for err, score in score_info
                         if err == "incomplete"]

    def middle_value(vals: list):
        """Returns the middle value from a sortable list.

        This is like the median, but assumes the list has an odd number of elements."""
        s = sorted(vals)
        return s[len(s) // 2]
        
    return middle_value(incomplete_scores)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=10)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
