"""Solves day 22, Advent of Code 2021."""

from aocd.models import Puzzle
from parse import parse
from collections import namedtuple
import numpy as np


# a Cuboid specifies a set of integer coordinate points {(x,y,z)}
# in the inclusive ranges given: i.e., x1 <= x <= x2, etc.
Cuboid = namedtuple("Cuboid", "x1 x2 y1 y2 z1 z2")

# a RebootStep is an instruction to put the points of a cuboid
# into a state of "on" or "off".
RebootStep = namedtuple("RebootStep", "state cuboid")


def parse_reboot_step(line: str) -> RebootStep:
    """Returns a reboot step."""
    p = parse("{} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}", line)
    return RebootStep(p[0], Cuboid(*p[1:]))


def parse_input_data(input_data: str) -> list:
    """Returns a list of reboot steps."""
    return [parse_reboot_step(line) for line in input_data.split('\n')]


def make_init_region() -> np.array:
    """Returns an initialization region."""
    pass


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    return "Solution not implemented"


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    return "Solution not implemented"


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=22)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
