"""Solves adventofcode/2021/day/4"""

from aocd.models import Puzzle
import numpy as np


def process_input(input_data: str) -> (list, list):
    """Convert input data string to drawn numbers and boards."""

    data = input_data.split("\n\n")
    draws = [int(x) for x in data[0].split(",")]
    board_strings = data[1:]

    def board_string_to_array(bstr: str) -> np.array:
        """Convert a 5-line string to an array representing a board"""
        return np.array([line.split() for line in bstr.split("\n")], dtype=int)

    return draws, [board_string_to_array(s) for s in board_strings]


def winning_combos(board: np.array) -> list:
    """Return a list of the winning rows for a board.

    A winning row is represented as a set of ints.
    There are 12 winning rows in the returned list."""

    wins = []
    # horizontal wins
    wins.extend([set(board[n,:]) for n in range(5)])
    # vertical wins
    wins.extend([set(board[:,n]) for n in range(5)])
    return wins


def board_wins(draw_set: set, combos: list):
    """Returns true if a board has won, false otherwise.

    Takes a set of drawn numbers and a list of winning number sets
    for the board."""

    for c in combos:
        if c.difference(draw_set) == set():
            return True
    return False


def winning_draw(draws: list, board: np.array) -> (int, int):
    """Returns the draw index and score for which the given board wins.

    The draw number is zero-indexed.  If the board does not
    win by the end of the draws, then ValueError is raised."""
    combos = winning_combos(board)
    draw_set = set()
    for i, d in enumerate(draws):
        draw_set.add(d)
        if board_wins(draw_set, combos):
            board_numbers = set(board.flatten())
            unmarked_numbers = board_numbers.difference(draw_set)
            score = d * sum(unmarked_numbers)
            return i, score
    raise ValueError("Board has no winning draw number.")


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    draws, boards = process_input(input_data)
    wins = [winning_draw(draws, b) for b in boards]
    first_winning_score = sorted(wins)[0][1]

    return first_winning_score


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    draws, boards = process_input(input_data)
    wins = [winning_draw(draws, b) for b in boards]
    last_winning_score = sorted(wins)[-1][1]

    return last_winning_score


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=4)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
