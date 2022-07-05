"""Solves day 09, Advent of Code 2021."""

from aocd.models import Puzzle
import numpy as np
import math

class Heightmap():
    """Represents a rectangular heightmap."""
    def __init__(self, input_data: str):
        height_data = [list(line)
                      for line in input_data.split('\n')]
        self.heights = np.array(height_data, dtype=int)
        self.rows, self.cols = self.heights.shape

    def in_bounds(self, coord: tuple) -> bool:
        """Test if a coordinate is in bounds."""
        
        i, j = coord
        return (i >= 0 and i < self.rows and
                j >= 0 and j < self.cols)

    
    def in_bounds_alt(self, coord: tuple) -> bool:
        """Test if a coordinate is in bounds.

        (Fun method for arbitrary numbers of axes.)"""

        return all([idx >= 0 and idx < bound
                    for idx, bound
                    in zip(coord, self.heights.shape)])

    
    def adjacent_coords(self, coord: tuple) -> list:
        """Return a list of adjacent, in-bound coordinates."""
        i, j = coord
        return filter(self.in_bounds,
                      [(i - 1, j), (i + 1, j),
                       (i, j - 1), (i, j + 1)])

    
def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    hm = Heightmap(input_data)

    def is_low_point(coord):
        adjacent_heights = [hm.heights[adj]
                            for adj in hm.adjacent_coords(coord)]
        return hm.heights[coord] < min(adjacent_heights)
        
    low_points = [(i, j)
                  for i in range(hm.rows) for j in range(hm.cols)
                  if is_low_point((i,j))]

    def risk_level(coord):
        return 1 + hm.heights[coord]

    return sum(map(risk_level, low_points))


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    hm = Heightmap(input_data)
    visited = hm.heights == 9

    basins = []
    all_coords = ((i, j) for i in range(hm.rows) for j in range(hm.cols))
    for c in all_coords:
        if visited[c]:
            continue
        
        # found an unvisited coord: start a new basin and fill it
        # with adjacent unvisited coords.
        current_basin = []
        to_visit = [c]
        while len(to_visit) > 0:
            x = to_visit.pop()
            if visited[x]:
                continue
            current_basin.append(x)
            visited[x] = True
            to_visit.extend(hm.adjacent_coords(x))
        basins.append(current_basin)

    sorted_basin_lengths = sorted(map(len, basins))

    return math.prod(sorted_basin_lengths[-3:])


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=9)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
