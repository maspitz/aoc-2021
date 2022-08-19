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
#01.2.3.4.56#   hall state
###0#1#2#3###   room states
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
        if not destination_ready(s, room_number):
            continue
        path_clear, steps_to_room = path_to_room(s, hall_space, room_number)
        if not path_clear:
            continue
        


def destination_ready(s: State, room_number: int):
    """Returns True if the room is ready for amphipods to enter it.

    It is ready only if all the amphipods within it
    have the room as their destination."""
    
    room_occupants = s.room_states[room_number]
    return all(o == '.' or o == ROOM_ASSIGNMENT[room_number]
               for o in room_occupants)


def path_to_room(s: State, hall_space: int, room_number: int) -> tuple:
    """Returns True and the number of steps to reach the room from the hall.

    If the path is blocked, then returns (False, None)."""

    # TODO complete function.
    pass


##### OLDER STUFF, DELETE WHAT'S OBSOLETE #####
def paths_to_hall(state: str, room_space: int) -> list:
    """Returns a list of possible destinations and costs for an amphipod.

    The list has the form: [(hall_space_1, cost_1), ...]"""
    amphipod = state[room_space]
    step_cost = STEP_COSTS[amphipod]
    steps = 0

    # first, step within the room if necessary
    if room_space > 10:
        if state[room_space - 4] != ".":
            return []
        room_space -= 4
        steps = 1

    dests = []
        
    # add hall locations reachable to the left
    hall_left = room_space - 6
    hall_left_steps = steps + 2
    while hall_left >= 0 and state[hall_left] == ".":
        dests.append((hall_left, hall_left_steps * step_cost))
        if hall_left > 1:
            hall_left_steps += 2
        else:
            hall_left_steps += 1
        hall_left -= 1

    # add hall locations reachable to the right
    hall_right = room_space - 5
    hall_right_steps = steps + 2
    while hall_right <= 6 and state[hall_right] == ".":
        dests.append((hall_right, hall_right_steps * step_cost))
        if hall_right < 5:
            hall_right_steps += 2
        else:
            hall_right_steps += 1
        hall_right += 1

    return dests


def cost_to_room(state: str, hall_space: int) -> tuple:
    """Returns the room destination and cost for an amphipod in the hall.

    The tuple has the form: (room_space, cost)
    If the destination is blocked, then the cost is infinite (math.inf)."""

    amphipod = state[hall_space]

    # start with dest set to outer destination (nearer the hallway)
    dest = DESTINATIONS[amphipod][0]

    # set waypoint hallway destination
    hall_dest = dest - 6
    if hall_dest < hall_space:
        hall_dest += 1

    # check room occupation.  set dest to inner room if appropriate.
    if state[dest] != '.':
        # outer room space is occupied; unreachable dest
        return (dest, math.inf)
    elif state[dest+4] == '.':
        # inner and outer room unoccupied; set dest to inner
        dest = dest + 4
    elif state[dest+4] != amphipod:
        # room contains an amphipod of another type; unreachable
        return (dest, math.inf)
    
    steps = 0
    
    # step to the left as needed
    while hall_space > hall_dest:
        if hall_space == 6:
            steps += 1
        else:
            steps += 2
        hall_space -= 1
        if state[hall_space] != '.':
            return (dest, math.inf)

    # step to the right as needed
    while hall_space < hall_dest:
        if hall_space == 0:
            steps += 1
        else:
            steps += 2
        hall_space += 1
        if state[hall_space] != '.':
            return (dest, math.inf)
        
    # step into room
    if dest <= 10:
        steps += 2
    else:
        steps += 3

    return (dest, steps * STEP_COSTS[amphipod])


GOAL_STATE = ".......ABCDABCD"

def amphipod_locations(state: str) -> tuple:
    """Returns the hall and room locations of amphipods to be organized."""
    hall_locs = [i for i in range(7) if state[i] != '.']
    room_locs_1 = [i for i in range(7, 11)
                   if (state[i] != '.' and
                       not ((state[i] == GOAL_STATE[i]) and
                            (state[i+4] == GOAL_STATE[i])))]
    room_locs_2 = [i for i in range(11, 15)
                   if state[i] != '.' and state[i] != GOAL_STATE[i]]
    return hall_locs, room_locs_1 + room_locs_2


def move(state: str, i: int, j: int) -> str:
    """Returns the state obtained by moving an amphipod from i to j."""
    if i < j:
        return state[:i] + state[j] + state[i+1:j] + state[i] + state[j+1:]
    elif j < i:        
        return state[:j] + state[i] + state[j+1:i] + state[j] + state[i+1:]
    else:
        raise ValueError("Tried to move an amphipod to itself.")


def min_organize_cost(state: str, _cache = {GOAL_STATE: 0}) -> int:
    """Returns the minimum movement cost to organize from a state."""
    if state in _cache:
        return _cache[state]
    hall_amphipods, room_amphipods = amphipod_locations(state)
    min_cost = math.inf

    for h in hall_amphipods:
        # try moving amphipod at h to its destination
        dest, move_cost = cost_to_room(state, h)
        if move_cost >= min_cost:
            continue
        trial_state = move(state, h, dest)
        trial_cost = move_cost + min_organize_cost(trial_state)
        min_cost = min(min_cost, trial_cost)

    for r in room_amphipods:
        # try moving amphipod at r to each possible space in the hall.
        paths = paths_to_hall(state, r)
        for dest, move_cost in paths:
            if move_cost >= min_cost:
                continue
            trial_state = move(state, r, dest)
            trial_cost = move_cost + min_organize_cost(trial_state)
            min_cost = min(min_cost, trial_cost)

    _cache[state] = min_cost
    return min_cost


    
def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    return "Solution not implemented"


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    return "Solution not implemented"


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=23)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
