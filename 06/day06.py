"""Solves day 06, Advent of Code 2021."""

from aocd.models import Puzzle


def get_fish(input_data: str) -> list:
    """Returns the fish population determined by the input string.

    The returned list is essentially a histogram of the fish timers."""

    ages = [int(n) for n in input_data.split(",")]
    fish = [0] * 9
    for a in ages:
        fish[a] += 1
    return fish


def advance_day(fish: list) -> list:
    """Given one day's fish population, return the next day's population."""

    # rotate the histogram of fish timers
    # so that nonzero timers are decremented by 1
    # and timers of 0 are sent to 8 (accounting for the new fish).

    new_fish = fish[1:] + fish[0:1]

    # add sufficient timers set to 6 to account for the resetting of
    # timers that had been set to 0.

    new_fish[6] += new_fish[8]

    return new_fish


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    fish = get_fish(input_data)
    for _ in range(80):
        fish = advance_day(fish)
    return sum(fish)


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    fish = get_fish(input_data)
    for _ in range(256):
        fish = advance_day(fish)
    return sum(fish)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=6)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
