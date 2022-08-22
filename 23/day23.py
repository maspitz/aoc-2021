"""Solves day 23, Advent of Code 2021."""

import math
from aocd.models import Puzzle
from parse import parse
from collections import namedtuple


"""The full state is a tuple of one hall state and four room states.

The hall state is a 7-character string containing elements '.ABCD'
which denote the occupation of the hall spaces where amphipods may stop.

A room state is a similar string of 2 or 4 characters for part A or B.

The indices correspond to the map:

#############
#012345678910#   hall state numbering
###0#1#2#3###   room state numbering
#############

There is no advantage to an amphipod's leaving its destination once it has
arrived.  We can say that it has arrived because the destination room does not
contain amphipods of any other type.  Combining this observation with the rules
of movement, we can conclude that in a minimal cost solution each amphipod can
move either zero times (if it's already at its destination and has no amphipods
of another type further in the room) or two times (once into a hall space and
once into a destination room space).
"""

State = namedtuple("State","hall_state room_states")

def parse_input_data(input_data: str) -> State:
    """Returns the problem state specified by the input."""
    input_format = """#############
#...........#
###{}#{}#{}#{}###
  #{}#{}#{}#{}#
  #########"""

    p = parse(input_format, input_data)
    if p == None:
        raise ValueError(f"Couldn't parse input: {input_data}")
    return State(hall_state="...........",
                 room_states=(p[0]+p[4],
                              p[1]+p[5],
                              p[2]+p[6],
                              p[3]+p[7]))

def print_state(s: State):
    """Prints a human-readable representation of the state."""
    print(s.hall_state)
    # I did it this way because zip didn't seem to act on a string as an iterable. (?)
    for j in range(len(s.room_states[0])):
        line = " "
        for rs in s.room_states:
            line += " " + rs[j]
        print(line)


def augment_room_states(s: State, folded: str):
    """Inserts the folded lines to the room states for part B."""
    new_room_states = tuple(rs[0] + fld + rs[-1]
                            for rs, fld in zip(s.room_states, folded))
    return State(s.hall_state,
                 new_room_states)


DESTINATION_ROOM = {"A": 0, "B": 1, "C": 2, "D": 3}
ROOM_ASSIGNMENT = (".A", ".B", ".C", ".D")

STEP_COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}


def in_front_of_room(hall_idx: int) -> bool:
    """Returns True if the hall location is in front of a room."""
    return hall_idx in (2, 4, 6, 8)


def hall_path_to_room(s: State, hall_idx: int, room_idx: int) -> str:
    """Returns a path from a hall location to a room."""
    hall_dest_idx = (room_idx + 1) * 2
    if hall_idx < hall_dest_idx:
        return s.hall_state[hall_idx+1:hall_dest_idx+1]
    else:
        return s.hall_state[hall_dest_idx:hall_idx]

def all_moves(s: State) -> list:
    """Returns a list of possible moves.

    The list takes the form: [(new_state_1, move_cost_1), ...]"""

    moves = []
    for hall_space, occupant in enumerate(s.hall_state):
        if occupant == '.':
            continue
        room_number = DESTINATION_ROOM[occupant]
        if not ready_to_fill_room(s, room_number):
            continue
        room_state = s.room_states[room_number]
        room_steps = room_state.count('.')        
        hall_path = hall_path_to_room(s, hall_space, room_number)
        hall_steps = len(hall_path)
        if hall_path != '.' * hall_steps:
            continue
        new_state = swap_occupant(s, hall_space, room_number, room_steps - 1)
        stepcost = STEP_COSTS[occupant]
        moves.append((new_state, (hall_steps + room_steps)*stepcost))

    def append_hall_moves(r: range):
        """Append moves from the room to any available hall locations in the range."""
        hall_steps = 0
        for hall_loc in r:
            hall_steps += 1
            if in_front_of_room(hall_loc):
                continue
            if s.hall_state[hall_loc] != '.':
                return
            new_state = swap_occupant(s, hall_loc, room_number, occupant_idx)
            moves.append((new_state, (hall_steps + room_steps)*stepcosts))
    
    for room_number, room_state in enumerate(s.room_states):
        # don't let an occupant leave a room that's ready to be filled
        if ready_to_fill_room(s, room_number):
            continue
        occupant_idx = room_state.count('.')
        if occupant_idx == len(room_state):
            continue
        occupant = room_state[occupant_idx]
        room_steps = occupant_idx + 1
        hall_idx = (room_number + 1) * 2
        stepcosts = STEP_COSTS[occupant]
        append_hall_moves(range(hall_idx + 1, 11))
        append_hall_moves(range(hall_idx - 1, -1, -1))
    return moves


def swap_occupant(s: State, hall_idx: int, room_num: int, room_idx: int) -> State:
    """Returns the state that swaps an amphipod between a hall and room location."""
    room_state = s.room_states[room_num]
    room_occupant = room_state[room_idx]
    hall_occupant = s.hall_state[hall_idx]
    return State(s.hall_state[:hall_idx] + room_occupant + s.hall_state[hall_idx + 1:],
                 s.room_states[:room_num] + (room_state[:room_idx] +
                                             hall_occupant +
                                             room_state[room_idx+1:],) +
                 s.room_states[room_num+1:])


def ready_to_fill_room(s: State, room_number: int) -> bool:
    """Returns True if the occupant can enter the destination room.

    It is ready only if all the room's occupants are of the
    proper destination occupant type."""

    return all(c in ROOM_ASSIGNMENT[room_number]
               for c in s.room_states[room_number])


INPUT_GOAL_A = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""


GOAL_STATE_A = parse_input_data(INPUT_GOAL_A)
GOAL_STATE_B = augment_room_states(GOAL_STATE_A, ("AA","BB","CC","DD"))


def min_organize_cost(s: State, _cache = {GOAL_STATE_A: 0, GOAL_STATE_B: 0}) -> int:
    """Returns the minimum movement cost to the goal state from a given state."""
    if s in _cache:
        return _cache[s]
    
    min_cost = math.inf
    for new_state, move_cost in all_moves(s):
        trial_cost = min_organize_cost(new_state) + move_cost
        min_cost = min(min_cost, trial_cost)

    _cache[s] = min_cost
    return min_cost

    
def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    s = parse_input_data(input_data)
    return min_organize_cost(s)


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""
    folded_state = parse_input_data(input_data)
    full_state = augment_room_states(folded_state, ("DD", "CB", "BA", "AC"))
    return min_organize_cost(full_state)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=23)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
