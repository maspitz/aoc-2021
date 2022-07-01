"""Solves day 07, Advent of Code 2021."""

from aocd.models import Puzzle
import numpy as np
import math


def get_crabs(input_data: str) -> list:
    """Provides a list of crab positions."""
    return [int(x) for x in input_data.split(",")]


"""Justification for the solution of part A.

For a number x0, let L(x0), M(x0), R(x0) be the total numbers
of crabs having coordinates x < x0, x = x0, or x > x0 respectively.
Let N be the total number of crabs.

Let V(x0) be the cost at integer coordinate x0.

Consider shifting to a coordinate one greater or less than x0,
thereby shifting the total cost by +1 or -1 per crab.

Then V(x0 + 1) = V(x0) + L(x0) + M(x0) - R(x0)
               = N - 2R(x0), and
     V(x0 - 1) = V(x0) + R(x0) + M(x0) - L(x0)
               = N - 2L(x0).

Start with the minimum crab coordinate x.  Let x -> x + 1.
With each step, R(x) either remains the same or decreases, and
V(x + 1) <= V(x) until R(x) < N/2.

Similarly, starting with maximum x and letting x -> x - 1,
V(x - 1) <= V(x) until L(x) < N/2.

So there is only one region where V(x) is minimal, and it
is that region for which both L(x) + M(x) >= N/2
and R(x) + M(x) >= N/2.  (which is a range containing at
least one integer x).  The floor (or ceiling) of median xm
is located in this region.
"""


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    crabs = get_crabs(input_data)

    def cost(x0: int) -> int:
        """Total cost for a selection of x0."""
        return sum(abs(x - x0) for x in crabs)

    return cost(math.floor(np.median(crabs)))


"""To obtain the solution for part b,
Note that the cost for an individual crab is d*(d+1)/2 where d = x - x0,
with x0 being the integer parameter to be varied.

We need to find the x0 for which T(x0), the sum of the costs, is minimal.
Thus,
    T(x0) = sum_i((x_i - x0)^2)/2 + sum_i(x_i - x0)/2.

If we consider T(x0) as a continuous function, it is a parabola with
a global minimum.  Letting diff(T(x0), x0) = 0 we find
the minimum is at x0 = sum_i(x_i)/N + 1/2.  So the optimium integer-valued
x0 is either the floor or ceiling of this value.
"""


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    crabs = get_crabs(input_data)

    def cost(x0: int) -> int:
        """Total cost for a selection of x0."""
        return sum(abs(x - x0) * (1 + abs(x - x0)) // 2 for x in crabs)

    xm = np.mean(crabs)
    return min(cost(math.floor(xm)), cost(math.ceil(xm)))


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=7)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
