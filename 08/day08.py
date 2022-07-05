"""Solves day 08, Advent of Code 2021."""

from aocd.models import Puzzle
from functools import reduce

def get_segments(input_line: str) -> (list, list):
    """Returns the encoded pattern list and output list."""

    patterns, outputs = [
            [frozenset(word) for word in sentence.split()]
            for sentence in input_line.split('|')]

    return patterns, outputs


def pattern_dictionary(patterns: list) -> dict:
    """Returns a mapping of each pattern to its digit."""

    # Group digit codes by numbers of segments lit.
    
    lit_segs = dict()
    for p in patterns:
        n = len(p)
        if n not in lit_segs:
            lit_segs[n] = []
        lit_segs[n].append(p)

    code = dict()
    code[1] = lit_segs[2][0]
    code[4] = lit_segs[4][0]
    code[7] = lit_segs[3][0]
    code[8] = lit_segs[7][0]

    # Identify segment codes from known digit codes
    segs = dict()
    segs["a"] = code[7] - code[1]
    segs["bd"] = code[4] - code[1]

    # Digit 0 can be distinguished by removing segments b and d.
    code[0] = [x for x in lit_segs[6]
               if len(x - segs["bd"]) == 5][0]

    # Digit 5 can be distinguished by removing segs b and d.
    code[5] = [x for x in lit_segs[5]
               if len(x - segs["bd"]) == 3][0]

    # Deduce segment codes via set operations.
    segs["d"] = code[4] - code[0]
    segs["b"] = segs["bd"] - segs["d"]
    segs["f"] = code[1] & code[5]
    segs["c"] = code[1] - segs["f"]
    segs["g"] = code[5] - (segs["a"] | code[4])
    segs["e"] = code[8] - (code[5] | segs["c"])

    # Construct remaining digit codes.
    def segment_unions(segstr: str) -> set:
        return frozenset.union(*(segs[s] for s in segstr))

    code[2] = segment_unions("acdeg")
    code[3] = segment_unions("acdfg")
    code[6] = segment_unions("abdefg")
    code[9] = segment_unions("abcdfg")

    return {code[digit]: digit for digit in range(10)}


def count_digits_1478(input_line: str) -> int:
    """Returns the total number of [1478] digits encoded in input_line."""

    patterns, outputs = get_segments(input_line)

    # digits 1,4,7,8 use 2,4,3,7 segments each.
    count_segs_2347 = [1 for code in outputs
                       if len(code) in {2, 4, 3, 7}]
    return sum(count_segs_2347)


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    return sum(map(count_digits_1478, input_data.split('\n')))
               

def decode_output(input_line: str) -> int:
               
    """Return the 4-digit output value encoded in a line."""

    patterns, outputs = get_segments(input_line)
    pd = pattern_dictionary(patterns)
    output_digits = [pd[o] for o in outputs]
    return reduce(lambda a, b: a * 10 + b, output_digits)
               
def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    return sum(map(decode_output, input_data.split('\n')))


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=8)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
