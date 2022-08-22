"""Solves day 23, Advent of Code 2021."""

from aocd.models import Puzzle
from parse import parse
from collections import namedtuple


"""The full state is a tuple of one hall state and four room states.

The hall state is a 7-character string containing elements '.ABCD'
which denote the occupation of the hall spaces where amphipods may stop.

A room state is a similar string of 2 or 4 characters for part A or B.

The indices correspond to the map:

#############
#01.2.3.4.56#   hall state numbering
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
    input_format = """#############
#...........#
###{}#{}#{}#{}###
  #{}#{}#{}#{}#
  #########"""

    p = parse(input_format, input_data)
    if p == None:
        raise ValueError(f"Couldn't parse input: {input_data}")
    return State(hall_state="."*7,
                 room_states=(p[0]+p[4],
                              p[1]+p[5],
                              p[2]+p[6],
                              p[3]+p[7]))


def include_folded_state(s: State, folded: str):
    """Adds the folded lines to the amphipod state for part B."""
    folded = ("DD", "CB", "BA", "AC")
    new_room_states = (rs[0] + fld + rs[1]
                       for rs, fld in zip(s.room_states, folded))
    return State(s.hall_state,
                 new_room_states)


DESTINATION_ROOM = {"A": 0, "B": 1, "C": 2, "D": 3}
ROOM_ASSIGNMENT = "ABCD"

STEP_COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}

def all_moves(s: State) -> list:
    """Returns a list of possible moves.

    The list takes the form: [(new_state_1, move_cost_1), ...]"""

    moves = []
    for hall_space, occupant in enumerate(s.hall_state):
        if occupant == '.':
            continue
        room_number = DESTINATION_ROOM[occupant]
        room_state = s.room_states[room_number]
        if not destination_ready(room_state, occupant):
            continue
        path_clear, hall_steps = path_to_room(s.hall_state,
                                              hall_space, room_number)
        if not path_clear:
            continue
        new_hall_state = remove_from_hall(s.hall_state, hall_space)
        new_room_state, room_steps = add_to_room(room_state, occupant)
        new_room_states = (s.room_states[:room_number] +
                           (new_room_state,) +
                           s.room_states[room_number+1:])
        new_state = State(new_hall_state, new_room_states)
        move_cost = (hall_steps + room_steps) * STEP_COSTS[occupant]
        moves.append((new_state, move_cost))
        
    for room_number, room_state in enumerate(s.room_states):
        pass  # FIXME
    breakpoint()
    return moves


def add_to_room(room_state: str, occupant: str) -> str:
    """Returns a room state with new occupant added and number of steps."""

    idx = room_state.rfind('.')
    if idx == -1:
        raise ValueError(f"Can't add {occupant=} to {room_state=}")
    return (room_state[:idx] + occupant + room_state[idx+1:],
            idx + 1)

def remove_from_hall(hall_state: str, hall_space: int) -> str:
    """Removes an amphipod from the hall."""

    return hall_state[:hall_space] + "." + hall_state[hall_space+1:]


def destination_ready(room_state: str, occupant: str) -> bool:
    """Returns True if the occupant can enter the destination room.

    It is ready only if all the room's occupants are of the
    proper destination occupant type."""

    return all(c == '.' or c == occupant for c in room_state)

# alternative empty hall check:
# EMPTY_HALL = "......."

def path_to_room(hall_state: str, hall_space: int, room_number: int) -> tuple:
    """Returns True and the number of steps to reach the room.

    The starting space is in the hall, indexed by hall_space.
    The ending space is just outside the room of the given room_number.
    If the path is blocked, then it returns (False, None)."""
    if hall_space <= room_number + 1:
        # need to move to the right
        if not all(c == '.' for c in hall_state[hall_space+1:room_number+2]):
            return (False, None)
        steps = (room_number - hall_space) * 2 + 3
        if hall_space == 0:
            steps -= 1
    else:
        # need to move to the left
        if not all(c == '.' for c in hall_state[room_number+2:hall_space]):
            return (False, None)
        steps = (hall_space - room_number) * 2 - 3
        if hall_space == 6:
            steps -= 1
    return (True, steps)


GOAL_STATE_A = State(".......",("AA", "BB", "CC", "DD"))
GOAL_STATE_B = State(".......",("AAAA", "BBBB", "CCCC", "DDDD"))


def min_organize_cost(s: State, _cache = {GOAL_STATE_A: 0}) -> int:
    """Returns the minimum movement cost to organize from a state."""
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

    return "Solution not implemented"


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=23)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
