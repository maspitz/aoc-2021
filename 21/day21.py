"""Solves day 21, Advent of Code 2021."""

from aocd.models import Puzzle
from parse import parse
from collections import namedtuple

def parse_input(input_data: str) -> (int, int):
    """Returns the starting positions of players 1 and 2."""

    return parse("Player 1 starting position: {:d}\n"
                 "Player 2 starting position: {:d}",
                 input_data).fixed


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    MAX_SCORE = 1000
    pos_1, pos_2 = parse_input(input_data)
    score_1, score_2 = 0, 0
    next_face = 1
    num_rolls = 0

    def roll_dice() -> int:
        """Returns the sum of three rolls while advancing the die state."""
        nonlocal next_face, num_rolls
        roll, next_face = next_face, (next_face % 100) + 1
        roll, next_face = roll + next_face, (next_face % 100) + 1
        roll, next_face = roll + next_face, (next_face % 100) + 1
        num_rolls += 3
        return roll

    def advance_player(pos: int, score: int, roll: int) -> (int, int):
        """Returns the position and score of a player advanced by a roll."""
        pos = (pos + roll - 1) % 10 + 1
        return pos, score + pos
    
    while True:
        pos_1, score_1 = advance_player(pos_1, score_1, roll_dice())
        if score_1 >= MAX_SCORE:
            break
        pos_2, score_2 = advance_player(pos_2, score_2, roll_dice())
        if score_2 >= MAX_SCORE:
            break
    return min(score_1, score_2) * num_rolls


# || Dirac Dice ||
# We will always view 'player 1' as meaning 'the player who moves next',
# so that we don't have to track whose turn it is in the game state.
# This means however that we do have to switch the labels 1 <-> 2
# with every turn.

GameState = namedtuple("GameState", "pos_1 pos_2 score_1 score_2")


def dirac_dice(gs: GameState, _cache:dict={}) -> (int, int):
    """Returns the numbers of universes in which each player wins.

    Assumes player 1 moves next, and player 1's score is < 21."""

    if gs.score_2 >= 21:
        return (0, 1)

    if gs in _cache:
        return _cache[gs]

    def advance_player1(s: GameState, roll: int) -> GameState:
        """Returns a new state by applying a roll to player 1."""
        newpos = (s.pos_1 + roll - 1) % 10 + 1
        return GameState(pos_1=newpos, pos_2=s.pos_2,
                         score_1=s.score_1+newpos, score_2 = s.score_2)

    def swap_players(s: GameState) -> GameState:
        """Returns a state in which the player numbers are swapped."""
        return GameState(pos_1=s.pos_2, pos_2=s.pos_1,
                         score_1=s.score_2, score_2=s.score_1)

    # sum of three rolls of three-sided dice
    rolls = [3,4,5,6,7,8,9]

    # number of ways each sum can occur; needed for correct counting
    freqs = [1,3,6,7,6,3,1]

    raw_results = [dirac_dice(swap_players(advance_player1(gs, r)))
                   for r in rolls]
    
    # results adjusted for correct counting and switching player label
    results = [(f*rr[1], f*rr[0]) for f, rr in zip(freqs, raw_results)]
    wins_tuple = tuple(sum(wins) for wins in zip(*results))
    
    _cache[gs] = wins_tuple
    return wins_tuple


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    pos_1, pos_2 = parse_input(input_data)
    gs = GameState(pos_1=pos_1, pos_2=pos_2,
                   score_1=0, score_2=0)
    wins_1, wins_2 = dirac_dice(gs)
    return max(wins_1, wins_2)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=21)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
