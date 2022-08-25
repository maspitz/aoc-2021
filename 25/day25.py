"""Solves day 25, Advent of Code 2021."""

from aocd.models import Puzzle

import numpy as np


class Cucumbers():
    """Models the cumcumber herds using np.array.

    In the array, the entries mean:
      0: empty space
      1: east-heading cucumber
      2: south-heading cucumber

    0-axis: southward movement
    1-axis: eastward movement

    We handle movement by rolling a copy of the array along
    an axis to check whether movement will occur in that direction.

    Then we use boolean-valued indexing to update the array
    with any changes."""
    
    def __init__(self, input_data: str):
        """Initialize the cucumbers from the input data."""
        s = input_data.replace('.','0')
        s = s.replace('>','1')
        s = s.replace('v','2')
        self.chart = np.array([[digit for digit in line]
                               for line in s.split('\n')], dtype=int)

    def move_east(self) -> bool:
        """Move the eastward cucumbers.  Returns True if any moved."""
        east_step = np.roll(self.chart, shift=-1, axis=1)
        place_empty = (self.chart == 1) & (east_step == 0)
        place_east_cucumber = np.roll(place_empty, shift=1, axis=1)
        self.chart[place_empty] = 0
        self.chart[place_east_cucumber] = 1
        return np.any(place_east_cucumber)

    def move_south(self) -> bool:
        """Move the southward cucumbers.  Returns True if any moved."""
        south_step = np.roll(self.chart, shift=-1, axis=0)
        place_empty = (self.chart == 2) & (south_step == 0)
        place_south_cucumber = np.roll(place_empty, shift=1, axis=0)
        self.chart[place_empty] = 0
        self.chart[place_south_cucumber] = 2
        return np.any(place_south_cucumber)
        

def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""
    c = Cucumbers(input_data)
    moves = 1
    while True:
        moved_east = c.move_east()
        moved_south = c.move_south()
        if not (moved_east or moved_south):
            return moves
        moves += 1


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=25)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")

