#!/usr/bin/env python3

from aocd.models import Puzzle
import numpy


def count_increases(vals: list[int]) -> int:
    "Return the number of times that the list members increase successively."
    num_incs = 0
    prev_val = vals[0]
    for v in vals[1:]:
        if v > prev_val:
            num_incs += 1
        prev_val = v
    return num_incs


def count_increases_numpy(vals: list[int]) -> int:
    """
    Return the number of times that the list members increase successively.

    Works by substracting two offset numpy.arrays
    and counting positive entries.
    """
    v = numpy.array(vals)
    return sum((v[1:] - v[:-1]) > 0)


def part_a(input_data: str) -> int:
    "Given the puzzle input data, return the solution for part A."
    depths = [int(line) for line in input_data.split('\n')]
    return count_increases(depths)


def part_b(input_data: str) -> int:
    "Given the puzzle input data, return the solution for part B."
    depths = [int(line) for line in input_data.split('\n')]
    d = numpy.array(depths)
    depth_windows = d[:-2] + d[1:-1] + d[2:]
    return count_increases(depth_windows)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=1)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
