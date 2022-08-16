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


class InitRegion():
    """Models a 50x50x50 initialization region."""

    def __init__(self):
        """Creates the initialization region."""
        self.data = np.zeros((101,101,101), dtype=int)

    def apply_step(self, r: RebootStep):
        """Applies a reboot step."""
        
        # translate reactor-core-coord range to np.array range,
        # keeping in mind that np.array range is x1 <= x < x2
        x1 = max(r.cuboid.x1+50, 0)
        x2 = min(r.cuboid.x2+51, 101)
        y1 = max(r.cuboid.y1+50, 0)
        y2 = min(r.cuboid.y2+51, 101)
        z1 = max(r.cuboid.z1+50, 0)
        z2 = min(r.cuboid.z2+51, 101)
        if r.state == "on":
            value = 1
        elif r.state == "off":
            value = 0
        else:
            raise ValueError(f"Unknown state: '{r.state}'")
        self.data[x1:x2,y1:y2,z1:z2] = value
        

    def total_cubes_on(self) -> int:
        """Returns the number of cubes that are currently on."""
        return np.sum(self.data)


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    ir = InitRegion()
    for step in parse_input_data(input_data):
        ir.apply_step(step)
    return ir.total_cubes_on()


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    return "Solution not implemented"


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=22)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
