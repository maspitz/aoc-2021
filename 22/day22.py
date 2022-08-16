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


def cuboids_overlap(a: Cuboid, b: Cuboid) -> bool:
    """Returns True if the cuboids a and b overlap."""

    # A cuboid includes all points within the product of its axis ranges.

    # Hence the intersection of two cuboids is precisely the product of
    # the intersections of their axis ranges.

    # Thus, two cuboids overlap if and only if all of their axis ranges
    # overlap.

    return not (a.x2 < b.x1 or b.x2 < a.x1 or
                a.y2 < b.y1 or b.y2 < a.y1 or
                a.z2 < b.z1 or b.z2 < a.z1)

def cuboid_difference(a: Cuboid, b: Cuboid) -> list:
    """Returns a list of cuboids containing all points in a and not b."""

    # Let cuboid C be the intersection of A and B.

    c = Cuboid(max(a.x1, b.x1), min(a.x2, b.x2),
               max(a.y1, b.y1), min(a.y2, b.y2),
               max(a.z1, b.z1), min(a.z2, b.z2))

    # Partition A into 27 cuboids, including C.

    partition_list = []
            
    def divide_range(a_1: int, a_2: int, c_1: int, c_2: int) -> tuple:
        """Divide the [a_1, a_2] range into three pieces."""
        return ((a.x1, c.x1 - 1), (c.x1, c.x2), (c.x2 + 1, a.x2))

    xlo, xmid, xhi = divide_range(a.x1, a.x2, c.x1, c.x2)
    ylo, ymid, yhi = divide_range(a.y1, a.y2, c.y1, c.y2)
    zlo, zmid, zhi = divide_range(a.z1, a.z2, c.z1, c.z2)

    def add_cuboid(d: Cuboid):
        # Append non-empty cuboids to a list.
        if (d.x1 <= d.x2 and
            d.y1 <= d.y2 and
            d.z1 <= d.z2):
            partition_list.append(d)

    # Add cuboids making up (A minus C) to the list

    add_cuboid(Cuboid(*xlo, *ylo, *zlo))
    add_cuboid(Cuboid(*xmid, *ylo, *zlo))
    add_cuboid(Cuboid(*xhi, *ylo, *zlo))
    add_cuboid(Cuboid(*xlo, *ymid, *zlo))
    add_cuboid(Cuboid(*xmid, *ymid, *zlo))
    add_cuboid(Cuboid(*xhi, *ymid, *zlo))
    add_cuboid(Cuboid(*xlo, *yhi, *zlo))
    add_cuboid(Cuboid(*xmid, *yhi, *zlo))
    add_cuboid(Cuboid(*xhi, *yhi, *zlo))
    add_cuboid(Cuboid(*xlo, *ylo, *zmid))
    add_cuboid(Cuboid(*xmid, *ylo, *zmid))
    add_cuboid(Cuboid(*xhi, *ylo, *zmid))
    add_cuboid(Cuboid(*xlo, *ymid, *zmid))
    # We do not add (*xmid, *ymid, *zmid) because that is C.
    add_cuboid(Cuboid(*xhi, *ymid, *zmid))
    add_cuboid(Cuboid(*xlo, *yhi, *zmid))
    add_cuboid(Cuboid(*xmid, *yhi, *zmid))
    add_cuboid(Cuboid(*xhi, *yhi, *zmid))
    add_cuboid(Cuboid(*xlo, *ylo, *zhi))
    add_cuboid(Cuboid(*xmid, *ylo, *zhi))
    add_cuboid(Cuboid(*xhi, *ylo, *zhi))
    add_cuboid(Cuboid(*xlo, *ymid, *zhi))
    add_cuboid(Cuboid(*xmid, *ymid, *zhi))
    add_cuboid(Cuboid(*xhi, *ymid, *zhi))
    add_cuboid(Cuboid(*xlo, *yhi, *zhi))
    add_cuboid(Cuboid(*xmid, *yhi, *zhi))
    add_cuboid(Cuboid(*xhi, *yhi, *zhi))

    return partition_list


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    return "Solution not implemented"


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=22)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
