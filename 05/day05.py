"""Solves day 05, Advent of Code 2021."""

import numpy as np
from aocd.models import Puzzle
from parse import parse
from collections import namedtuple

Segment = namedtuple("Segment", "x1 y1 x2 y2")

def get_segments(input_data: str) -> list:
    """Convert input data string into a list of Segments."""

    data = [parse("{x1:d},{y1:d} -> {x2:d},{y2:d}", line).named
            for line in input_data.split("\n")]
    return [Segment(**d) for d in data]


def make_field(segments: list) -> np.array:
    """Make an empty field large enough for the given Segments."""

    max_x, max_y = 0, 0
    for s in segments:
        max_x = max(max_x, s.x1, s.x2)
        max_y = max(max_y, s.y1, s.y2)
        if min(s.x1, s.x2, s.y1, s.y2) < 0:
            raise ValueError("Segment has a negative coordinate")
    return np.zeros([max_x + 1, max_y + 1])


def add_segment_to_field(seg: Segment, field: np.array, allow_diagonal=False):
    """Modifies the provided field by incrementing the points along the segment.

    If allow_diagonal is false, then diagonal segments will be ignored."""

    def inclusive_range(a1, a2):
        if a1 < a2:
            return list(range(a1, a2 + 1))
        else:
            return list(range(a1, a2 - 1, -1))

    x_range = inclusive_range(seg.x1, seg.x2)
    y_range = inclusive_range(seg.y1, seg.y2)

    # zip the ranges into seg_range
    if len(x_range) == 1:
        seg_range = zip(x_range * len(y_range), y_range)
    elif len(y_range) == 1:
        seg_range = zip(x_range, y_range * len(x_range))
    elif not allow_diagonal:
        return None
    elif len(x_range) == len(y_range):
        seg_range = zip(x_range, y_range)
    else:
        return ValueError("Segment has unequal diagonal offsets")

    for x, y in seg_range:
        field[x][y] += 1


def count_overlaps(field: np.array) -> int:
    """Count the number of field values that are at least 2."""

    return np.sum(field >= 2)


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    segments = get_segments(input_data)
    field = make_field(segments)
    for s in segments:
        add_segment_to_field(s, field, allow_diagonal=False)
    return count_overlaps(field)


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    segments = get_segments(input_data)
    field = make_field(segments)
    for s in segments:
        add_segment_to_field(s, field, allow_diagonal=True)
    return count_overlaps(field)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=5)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
