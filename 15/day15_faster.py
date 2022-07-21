"""Solves day 15, Advent of Code 2021.

This is not an alternative method, but a modification of my day15.py.
It still uses Dijkstra's with heapq, but there are a few optimizations
to cut the running time by roughly 40%."""

from aocd.models import Puzzle
import heapq
import numpy as np
from dataclasses import dataclass

INFTY = float("inf")

# input data for the puzzle is 100x100, hence:
#  10,000 nodes, and about 40,000 edges.


@dataclass
class Graph:
    """Models a graph."""
    nodes: int
    rows: int
    cols: int
    weights: list
    def edges(self, node: int) -> list:
        """Return the edges from a given node."""
        row = node // self.cols
        col = node % self.cols
        if row > 0 and row < self.rows - 1 and col > 0 and col < self.cols - 1:
            return [node - self.cols, node - 1, node + 1, node + self.cols]
        else:
            e = []
            if row > 0: e.append(node - self.cols)
            if col > 0: e.append(node - 1)
            if col < self.cols - 1: e.append(node + 1)
            if row < self.rows - 1: e.append(node + self.cols)
            return e


def parse_multiline_digits(input_data: str) -> np.array:
    """Read multiline digits into numpy array."""

    digits = [[d for d in line]
              for line in input_data.split()]
    return np.array(digits, dtype=int)


def augment_array(small_array: np.array, times: int) -> np.array:
    """Create larger array from smaller as per day 15 problem.

    Namely, the array is duplicated, digits are incremented by one,
    with 10 wrapping to 1, and duplicates are stacked horizontally
    and vertically."""

    def increment_array(a: np.array) -> np.array:
        """Return new array incremented by 1, wrapping 10 to 1."""
        b = (a + 1) % 10
        b[b == 0] = 1
        return b

    work = small_array.copy()
    inc_array = small_array.copy()
    for x in range(times - 1):
        inc_array = increment_array(inc_array)
        work = np.hstack((work, inc_array))

    inc_array = work.copy()
    for y in range(times - 1):
        inc_array = increment_array(inc_array)
        work = np.vstack((work, inc_array))

    return work
    

def make_graph(input_array: np.array) -> Graph:
    """Convert 2d array of arrival weights into rectangular graph."""

    rows, cols = np.shape(input_array)
    nodes = rows * cols
    edges = [None for x in range(nodes)]
    costs = input_array.flatten()

    return Graph(nodes=nodes, rows=rows, cols=cols, weights=costs)


def dijkstra(g: Graph, start, finish) -> int:
    """Return the cost of minimum-cost path from start to finish.

    Uses Dijkstra's algorithm with min-heap priority queue.
    """

    visited_nodes = [False] * g.nodes
    
    # tracking the best cost from each visited node
    cost = [INFTY] * g.nodes

    cost[start] = 0
    
    # to_visit is a heapified list containing tuples of (cost, node),
    # where cost is the best code for that node when added to the heap.
    
    to_visit = [(0, start)]
    
    while to_visit:
        node_cost, node = heapq.heappop(to_visit)
        if visited_nodes[node]:
            continue
        visited_nodes[node] = True
        for neighbor in g.edges(node):
            trial_cost = node_cost + g.weights[neighbor]
            if trial_cost < cost[neighbor]:
                cost[neighbor] = trial_cost
                heapq.heappush(to_visit, (trial_cost, neighbor))
    return cost[finish]


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    a = parse_multiline_digits(input_data)
    g = make_graph(a)
    return dijkstra(g, 0, g.nodes - 1)

def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    a = parse_multiline_digits(input_data)
    a = augment_array(a, 5)
    g = make_graph(a)
    return dijkstra(g, 0, g.nodes - 1)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=15)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
