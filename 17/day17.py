"""Solves day 17, Advent of Code 2021."""

from aocd.models import Puzzle
from collections import defaultdict
from parse import parse
import math

"""
Notes on the problem.

I assume the target coordinates have: 0 < x1 < x2  and  y2 < y1 < 0,
as in the example.

The dynamics of x and y are decoupled and we can determine them explicitly:

For i >= 0:

y(i+1) = y(i) + vy(i),

vy(i+1) = vy(i) - 1

So:

vy(n) = vy(0) - n,

y(n) = sum_{i = 0}^{n} vy(i)
     = n*vy(0) - sum_{i=0}^{n} n
     = n*vy(0) - n*(n-1)/2

Similarly, for x > 0 and vx > 0,

vx(n) = max(0, vx(0) - n)
x(n) = n*vx(0) - n*(n-1)/2                for n <= vx(0)
     = vx(0)*(vx(0) + 1) / 2              for n > vx(0)

"""

def step_at_x(x: int, vx: int) -> float:
    """Return the step at which the probe is at x.  (May return None.)"""

    disc = (.5 + vx)**2 - 2*x
    if disc < 0: return None
    return .5 + vx - math.sqrt(disc)


def step_at_y(y: int, vy: int) -> tuple:
    """Return the step at which the probe is at y."""
    # assumes y < 0
    disc = (.5 + vy)**2 - 2*y
    return .5 + vy + math.sqrt(disc)


def minimal_vx(x: int) -> float:
    """The minimum vx needed to ever reach x."""

    return (-1 + math.sqrt(1 + 8*x))/2

def maximal_vx(x: int) -> float:
    """The maximal vx that reaches x no earlier than step 1."""
    return x

def x_range_in_target(x1: int, x2: int) -> dict:
    """Returns a mapping from x-velocities to a step-range-pair.

    By step-range-pair, I mean a tuple (s1, s2) such that
    the probe's x is within the range [x1, x2] during
    the interval [s1, s2]."""

    ans = {}
    for vx in range(math.floor(minimal_vx(x1)),
                    math.floor(maximal_vx(x2)) + 1):
        s1 = step_at_x(x1, vx)
        s2 = step_at_x(x2, vx)
        if s1 is None:
            continue
        else:
            s1 = math.ceil(s1)
        if s2 is None:
            s2 = math.inf
        else:
            s2 = math.floor(s2)
        if s1 <= s2:
            ans[vx] = (s1, s2)
    return ans


def minimal_vy(y1: int) -> float:
    """The minimal (most negative) vy that reaches y1 no earlier than step 1."""
    # recall that we assume a target such that y1 < 0.
    return y1

def maximal_vy(y1: int) -> float:
    """The maximal (most positive) vy that does not overshoot y1 on the return going down."""
    return abs(y1)

def y_range_in_target(y1: int, y2: int) -> dict:
    """Returns a mapping from y-velocities to a step-range-pair.

    By step-range-pair, I mean a tuple (s1, s2) such that
    the probe's y is within the range [y1, y2] during
    the interval [s1, s2]."""

    ans = {}
    for vy in range(math.floor(minimal_vy(y1)),
                    math.floor(maximal_vy(y1)) + 1):
        s1 = step_at_y(y2, vy)
        s2 = step_at_y(y1, vy)
        s1 = math.ceil(s1)
        s2 = math.floor(s2)
        if s1 <= s2:
            ans[vy] = (s1, s2)
    return ans


def v_for_steps(range_in_target: dict) -> dict:
    """Returns a mapping from steps to a set of suitable velocity components.

    For example, if the probe is in the target at step 2 for precisely the x-velocities
    vx = 3 and vx = 4, then the returned dict would include the item {2: {3, 4}}
    """

    ans = defaultdict(set)
    for v, (s1, s2) in range_in_target.items():
        for step in range(s1, s2 + 1):
            ans[step] |= {v}
    return ans


def velocities_for_target(x1: int, x2: int, y1: int, y2: int) -> set:
    """Return the set of (vx, vy) that reach the target on some step."""

    yrt = y_range_in_target(y1, y2)
    vy_dict = v_for_steps(yrt)
    max_step = max(vy_dict.keys())
    
    xrt = x_range_in_target(x1, x2)
    # replace infinite values with max step value from y:
    xrt = {vx: (s1, min(max_step, s2))
           for (vx, (s1, s2)) in xrt.items()}
    vx_dict = v_for_steps(xrt)

    target_steps = vx_dict.keys() & vy_dict.keys()
    return {(vx, vy)
            for step in target_steps
            for vx in vx_dict[step]
            for vy in vy_dict[step]}


def parse_input_data(input_data: str) -> dict:
    """Return the target's specifications."""

    return parse('target area: x={x1:d}..{x2:d}, y={y1:d}..{y2:d}', input_data).named


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    vs = velocities_for_target(**parse_input_data(input_data))
    max_vy = max(vs, key=lambda x: x[1])[1]
    return max_vy * (max_vy + 1) // 2
    

def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    vs = velocities_for_target(**parse_input_data(input_data))
    return len(vs)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=17)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
