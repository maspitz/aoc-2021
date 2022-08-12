"""Solves day 20, Advent of Code 2021."""

from aocd.models import Puzzle
import numpy as np
from dataclasses import dataclass

@dataclass
class Image:
    """Represents the image that's being enhanced."""
    data: np.array
    background: int

    
def parse_input(input_data: str) -> (np.array, Image):
    """Returns the enhancement algorithm and the initial image."""
    alg_str = input_data[0:512]
    algorithm = np.array([c == '#' for c in alg_str], dtype=int)
    lines = input_data[512:].split()
    data = np.array([[c == '#' for c in line] for line in lines], dtype=int)
    return algorithm, Image(data=data, background=0)


def enhancement_index(e: np.array) -> np.array:
    """Given an (m+2)x(n+2) binary valued array, return a mxn index array.
    
    The index array contains the enhancement algorithm indices (as described
    in the problem statement) corresponding to the e[1:m+1,1:n+1] subarray."""
    
    m, n = e.shape
    return (1 * e[2:m, 2:n] + 2 * e[2:m, 1:n-1] + 4 * e[2:m, 0:n-2] +
            8 * e[1:m-1, 2:n] + 16 * e[1:m-1, 1:n-1] + 32 * e[1:m-1, 0:n-2] +
            64 * e[0:m-2, 2:n] + 128 * e[0:m-2, 1:n-1] + 256 * e[0:m-2, 0:n-2])
    
    
def enhance(algorithm: np.array, im: Image) -> Image:
    """Returns an enhanced image."""

    rows, cols = im.data.shape
    bkg_rows = np.full(shape=(2,cols), fill_value=im.background, dtype=int)
    bkg_cols = np.full(shape=(rows+4, 2), fill_value=im.background, dtype=int)
    enlarged_data = np.hstack([bkg_cols,
                               np.vstack([bkg_rows, im.data, bkg_rows]),
                               bkg_cols])
    e_index = enhancement_index(enlarged_data)

    new_data = algorithm[e_index]
    new_background = algorithm[511 * im.background]
    return Image(data = new_data, background = new_background)


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    al, im = parse_input(input_data)
    im = enhance(al, im)
    im = enhance(al, im)
    return im.data.sum()


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    al, im = parse_input(input_data)
    for count in range(50):
        im = enhance(al, im)
    return im.data.sum()


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=20)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
