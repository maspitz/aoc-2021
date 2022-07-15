"""Solves day 13, Advent of Code 2021."""

from aocd.models import Puzzle
from parse import parse
from collections import namedtuple
import numpy as np



Dot = namedtuple("Dot", "x y")


Instruction = namedtuple("Instruction", "axis intercept")


def parse_input(input_data: str) -> (set, list):
    """Returns a set of dots and a list of Instructions."""

    dots_str, instructions_str = input_data.split('\n\n')
    
    dots = {Dot(**parse("{x:d},{y:d}", line).named)
            for line in dots_str.split('\n')}

    instructions = [Instruction(**parse("fold along {axis}={intercept:d}", line).named)
                    for line in instructions_str.split('\n')]
    
    return dots, instructions


def apply_fold(dots: set, fold: Instruction) -> set:
    """Returns a new set of dots created by folding the input set of dots."""

    if fold.axis == "x":

        def folded_dot(d: Dot) -> Dot:
            if d.x > fold.intercept:
                return Dot(x=(2 * fold.intercept - d.x), y=d.y)
            return d
        
        return {folded_dot(d) for d in dots}

    if fold.axis == "y":

        def folded_dot(d: Dot) -> Dot:
            if d.y > fold.intercept:
                return Dot(x=d.x, y=(2 * fold.intercept - d.y))
            return d

        return {folded_dot(d) for d in dots}

    raise ValueError(f"Unknown fold axis: {fold.axis}")


def draw_dots(dots: set) -> str:
    """Returns a multiline string plotting a set of dots.

    The plot range is from (0,0) to the max x and max y of the dot set.
    Empty space is ' '.  Dots are '#'."""

    max_x = max(d.x for d in dots)
    max_y = max(d.y for d in dots)
    plot_str = ""
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if Dot(x,y) in dots:
                plot_str += "#"
            else:
                plot_str += " "
        plot_str += "\n"
    return plot_str


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    dots, instructions = parse_input(input_data)
    folded_dots = apply_fold(dots, instructions[0])
    return len(folded_dots)


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    dots, instructions = parse_input(input_data)
    for i in instructions:
        dots = apply_fold(dots, i)
    return draw_dots(dots)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=13)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: \n{part_b(puzzle.input_data)}")
