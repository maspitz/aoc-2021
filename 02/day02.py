#!/usr/bin/env python3

from aocd.models import Puzzle

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

    course = [line.split(' ') for line in input_data.split('\n')]
    horizontal, depth = 0, 0
    for heading, dist_str in course:
        dist = int(dist_str)
        if heading == "forward":
            horizontal += dist
        elif heading == "down":
            depth += dist
        elif heading == "up":
            depth -= dist
        else:
            raise ValueError(f"invalid heading: {heading}")
    return horizontal * depth


def part_b(input_data: str) -> int:
    "Given the puzzle input data, return the solution for part B."

    course = [line.split(' ') for line in input_data.split('\n')]
    horizontal, depth, aim = 0, 0, 0
    for heading, x_str in course:
        x = int(x_str)
        if heading == "forward":
            horizontal += x
            depth += aim * x
        elif heading == "down":
            aim += x
        elif heading == "up":
            aim -= x
        else:
            raise ValueError(f"invalid heading: {heading}")
    return horizontal * depth


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=2)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
