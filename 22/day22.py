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


def cuboid_intersection(a: Cuboid, b: Cuboid) -> Cuboid:
    """Return the intersection of A and B."""
    return Cuboid(max(a.x1, b.x1), min(a.x2, b.x2),
                  max(a.y1, b.y1), min(a.y2, b.y2),
                  max(a.z1, b.z1), min(a.z2, b.z2))


def divide_range(u1: int, u2: int, v1: int, v2: int) -> tuple:
    """Partition [u1, u2] based on intersection with [v1, v2]."""
    if u1 < v1:
        if u2 > v2:
            return ((u1, v1 - 1), (v1, v2), (v2 + 1, u2))
        else:
            return ((u1, v1 - 1), (v1, v2))
    elif u2 > v2:
        return ((v1, v2), (v2 + 1, u2))
    else:
        return ((v1, v2),)


def cuboid_difference(a: Cuboid, b: Cuboid) -> list:
    """Returns a list of cuboids containing all points in a and not b."""

    c = cuboid_intersection(a, b)
    
    # Partition A into 27 cuboids, including C.

    xranges = divide_range(a.x1, a.x2, c.x1, c.x2)
    yranges = divide_range(a.y1, a.y2, c.y1, c.y2)
    zranges = divide_range(a.z1, a.z2, c.z1, c.z2)

    cuboids = {Cuboid(*xrange, *yrange, *zrange)
               for xrange in xranges
               for yrange in yranges
               for zrange in zranges}

    return cuboids - {c}


def cuboid_volume(a: Cuboid) -> int:
    """Returns the number of points in a cuboid."""
    return ((a.x2 - a.x1 + 1) *
            (a.y2 - a.y1 + 1) *
            (a.z2 - a.z1 + 1))


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    active = set()
    # Loop invariant:
    # active is a set of nonoverlapping cuboids which contain
    # exactly those points which are currently turned on,
    # considering all the steps processed up to that iteration.

    for rbs in parse_input_data(input_data):
        # Find the cuboids that overlap this reboot step's cuboid.
        overlaps = {c for c in active
                    if cuboids_overlap(c, rbs.cuboid)}

        # Partition them into pieces excluding this step's cuboid.
        overlap_differences = [cuboid_difference(o, rbs.cuboid)
                               for o in overlaps]

        # Replace the overlapping cuboids with the nonoverlapping pieces.
        active -= overlaps
        active = set.union(active, *overlap_differences)
        
        # If this step's cuboid turns points on, then include it.
        if rbs.state == "on":
            active |= {rbs.cuboid}

    return sum(cuboid_volume(c) for c in active)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=22)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
