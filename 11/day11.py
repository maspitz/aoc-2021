"""Solves day 11, Advent of Code 2021."""

from aocd.models import Puzzle


def make_grid(input_data: str) -> list:
    """Converts input data string into a list of 100 ints."""

    return [int(ch) for ch in input_data if ch != '\n']


def neighbor_coords(x, y: int) -> list:
    """Returns a list of 8 neighbor coordinates."""
    return [(x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y), (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1)]


def print_grid(grid: list):
    """Prints a grid."""
    for y in range(10):
        print(grid[y*10:(y+1)*10])


def advance_grid(grid: list) -> list:
    """Returns a new grid advanced by one step."""

    next_grid = grid.copy()
    energy_gainers = [(x,y)
                      for x in range(10) for y in range(10)]
    while(energy_gainers):
        x, y = energy_gainers.pop()
        # ignore out-of-grid coordinates
        if (x < 0 or x > 9 or
            y < 0 or y > 9):
            continue
        # increment octopus on grid:
        c = x + y * 10
        next_grid[c] += 1
        # if it was increased to 10, then flash.
        if next_grid[c] == 10:
            energy_gainers.extend(neighbor_coords(x, y))

    # set flashed octopuses to 0.
    next_grid = [min(g, 10) % 10 for g in next_grid]
    return next_grid


def count_flashes(grid: list) -> int:
    """Returns the number of flashes from the previous step."""

    return sum(1 for octopus in grid if octopus == 0)


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    total_flashes = 0
    grid = make_grid(input_data)
    for step in range(100):
        grid = advance_grid(grid)
        total_flashes += count_flashes(grid)
    return total_flashes
        
    return "Solution not implemented"

def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""
    
    step = 0
    grid = make_grid(input_data)
    while True:
        grid = advance_grid(grid)
        step += 1
        if count_flashes(grid) == 100:
            return step


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=11)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
