"""Solves day 17, Advent of Code 2021.  Simulation-oriented."""

"""
This is a simulation-oriented solution to day 17.

Rather than using the explicit expressions for the probe positions
at a given time (as in day17.py solution), this method evolves the
probe position one step at a time.

Compared to the explicit method, this way takes a bit longer to run
but it's easier to understand.  Also, we could drop in a different
model for the probe's dynamics if we ever wanted to.
"""


from aocd.models import Puzzle
from collections import namedtuple
from parse import parse

State = namedtuple("State", "x y vx vy")

Target = namedtuple("Target", "xmin xmax ymin ymax")

def state_generator(s: State):
    """Provides a generator yielding the state for each step."""
    if s.vx >= 0:
        while True:
            yield s
            s = State(s.x + s.vx, s.y + s.vy, max(0, s.vx - 1), s.vy - 1)
    else:
        while True:
            yield s
            s = State(s.x + s.vx, s.y + s.vy, min(0, s.vx + 1), s.vy - 1)

def probe_in_target(s: State, t: Target) -> bool:
    """Tests whether the probe is within the target."""
    return ((t.xmin <= s.x <= t.xmax) and
            (t.ymin <= s.y <= t.ymax))

def probe_missed_target(s: State, t: Target) -> bool:
    """Tests for certain states that have over-or-undershot the target."""

    # undershot or overshot in x
    if s.vx == 0 and not (t.xmin <= s.x <= t.xmax): return True

    # overshot in x
    if s.vx >= 0 and s.x > t.xmax: return True
    if s.vx <= 0 and s.x < t.xmin: return True
    
    # falling below target
    if s.vy <= 0 and s.y < t.ymin: return True
    
    return False

def parse_input_data(input_data: str) -> Target:
    """Return the target's specifications."""

    data = parse('target area: x={x1:d}..{x2:d}, y={y1:d}..{y2:d}',
                 input_data).named
    return Target(xmin = min(data["x1"], data["x2"]),
                  xmax = max(data["x1"], data["x2"]),
                  ymin = min(data["y1"], data["y2"]),
                  ymax = max(data["y1"], data["y2"]))


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    # get target
    target = parse_input_data(input_data)
    if target.xmin <= 0 or target.ymax >= 0:
        raise ValueError(f"Unexpected target range: {target}")
    ymax_list = []
    for vx in range(1, target.xmax + 1):
        ymax = 0
        for vy in range(target.ymin, -target.ymin):
            sg = state_generator(State(x=0, y=0, vx=vx, vy=vy))
            for probe in sg:
                ymax = max(ymax, probe.y)
                if probe_in_target(probe, target):
                    ymax_list.append(ymax)
                    break
                if probe_missed_target(probe, target):
                    break
    return max(ymax_list)      


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    # get target
    target = parse_input_data(input_data)
    if target.xmin <= 0 or target.ymax >= 0:
        raise ValueError(f"Unexpected target range: {target}")
    v_list = []
    for vx in range(1, target.xmax + 1):
        for vy in range(target.ymin, -target.ymin):
            sg = state_generator(State(x=0, y=0, vx=vx, vy=vy))
            for probe in sg:
                if probe_in_target(probe, target):
                    v_list.append((vx, vy))
                    break
                if probe_missed_target(probe, target):
                    break
    return len(v_list)      


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=17)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
