"""Solves day 14, Advent of Code 2021."""

from aocd.models import Puzzle
from parse import parse
from collections import namedtuple, defaultdict


def parse_input(input_data: str) -> (str, list):
    """Returns the polymer template string and a list of insertion rules."""

    polymer_template, rules_lines = input_data.split('\n\n')
    rules = [parse("{} -> {}", line) for line in rules_lines.split('\n')]
    
    return polymer_template, rules


def get_polyset(polymer: str) -> defaultdict:
    """Returns an accounting of how many times each pair occurs in a polymer string.

    For example, polymer_pair_count('NNCB') yields:
    {'NN': 1, 'NC': 1, 'CB': 1}.
    """

    pair_count = defaultdict(int)
    for i in range(len(polymer) - 1):
        pair = polymer[i:i+2]
        pair_count[pair] += 1
    return pair_count


def pair_substitutions(rules: list) -> dict:
    """Returns a dict of substitutions prescribed by the rules list.

    For example, the rules CH -> B and HH -> N would yield:
    {"CH": ("CB", "BH"), "HH": ("HN", "NH")}
    """

    subs = dict()
    for r in rules:
        pair, elt = r
        if pair in subs:
            raise ValueError(f"Found two rules for pair {pair}")
        subs[pair] = (pair[0] + elt, elt + pair[1])
    return subs


def grow_polyset(polyset: defaultdict, sub_rules: dict) -> defaultdict:
    """Determines the polyset for the next step, given the substitution rules."""

    new_poly = defaultdict(int)
    for pair, count in polyset.items():
        pair_1, pair_2 = sub_rules[pair]
        new_poly[pair_1] += count
        new_poly[pair_2] += count
    return new_poly

def polyset_elements(polyset: defaultdict) -> defaultdict:
    """Returns a count of the elements in the polyset."""

    elt_count = defaultdict(int)
    for pair, count in polyset.items():
        for elt in pair:
            elt_count[elt] += count
    return elt_count


def polymer_quantity_difference(polyset: defaultdict, orig_polymer: str) -> int:
    """Returns the difference between quantities of the most and least common elements."""

    elt_count = polyset_elements(polyset)

    # Adjust the element count:
    # The polyset is made by splitting the polymer elements into pairs.
    # The first and last elements appear in only one pair in the polyset.
    # All other elements appear in two pairs, and are thus double-counted.
    # So: first increment the first and last elements so that everything is double-counted,
    # then divide everything by two to correct the element count.

    elt_count[orig_polymer[0]] += 1
    elt_count[orig_polymer[-1]] += 1
    elt_count = {elt: n // 2  for elt, n in elt_count.items()}

    return max(elt_count.values()) - min(elt_count.values())


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    polymer_template, rules = parse_input(input_data)
    polyset = get_polyset(polymer_template)
    sub_rules = pair_substitutions(rules)
    for x in range(10):
        polyset = grow_polyset(polyset, sub_rules)
    return polymer_quantity_difference(polyset, polymer_template)


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    polymer_template, rules = parse_input(input_data)
    polyset = get_polyset(polymer_template)
    sub_rules = pair_substitutions(rules)
    for x in range(40):
        polyset = grow_polyset(polyset, sub_rules)
    return polymer_quantity_difference(polyset, polymer_template)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=14)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
