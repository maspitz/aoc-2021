"""Solves day 18, Advent of Code 2021."""

"""
In this solution, I leave the snailfish number in serialized (aka string)
form except for the magnitude calculation.  The serialized form is
more convenient than tree form for the split and explode operations anyway.
"""


from aocd.models import Puzzle

def find_bracket_depth(s: str, depth: int) -> int:
    """Return the first index at which the bracket depth is found.

    Returns -1 if bracket depth is not found."""
    d = 0
    for idx, ch in enumerate(s):
        if ch == '[':
            d += 1
            if d == depth:
                return idx
        elif ch == ']':
            d -= 1
    return -1

def explode(s: str) -> str:
    """Returns an exploded snailfish number.

    Returns empty string if the number could not be exploded."""
    left_bracket = find_bracket_depth(s, 5)
    if left_bracket == -1:
        return ""
    comma = s.index(',', left_bracket + 1)
    right_bracket = s.index(']', comma + 1)
    left_value = int(s[left_bracket+1:comma])
    right_value = int(s[comma+1:right_bracket])
    for i in range(left_bracket - 1, -1, -1):
        if s[i] not in "[,]":
            break
    left_number_stop = i + 1
    for i in range(left_number_stop - 1, -1, -1):
        if s[i] in "[,]":
            break
    left_number_start = i + 1
    for i in range(right_bracket + 1, len(s)):
        if s[i] not in "[,]":
            break
    right_number_start = i
    for i in range(right_number_start, len(s)):
        if s[i] in "[,]":
            break
    right_number_stop = i
    if left_number_start < left_number_stop:
        left_number = int(s[left_number_start:left_number_stop])
        snailfish = (s[:left_number_start] +
                     str(left_number + left_value) +
                     s[left_number_stop:left_bracket] +
                     "0")
    else:
        snailfish = s[:left_bracket] + "0"
    if right_number_start < right_number_stop:
        right_number = int(s[right_number_start:right_number_stop])
        snailfish += (s[right_bracket+1:right_number_start] +
                      str(right_number + right_value) +
                      s[right_number_stop:])
    else:
        snailfish += s[right_bracket+1:]
    return snailfish

def split(s: str) -> str:
    """Returns an split snailfish number.

    Returns empty string if the number could not be split."""

    # find first multi-digit number
    n_digits = 0
    number_start = 0
    number_stop = 0
    for i, ch in enumerate(s):
        if ch in "[,]":
            if n_digits > 1:
                number_start = i - n_digits
                number_stop = i
                break
            n_digits = 0
        else:
            n_digits += 1
    if number_start == 0:
        return ""
    number = int(s[number_start:number_stop])
    left_value = number // 2
    right_value = number // 2 + number % 2
    return s[:number_start] + f"[{left_value},{right_value}]" + s[number_stop:]
            
def add(s1: str, s2: str) -> str:
    """Add two snailfish numbers, returning their sum."""

    return f"[{s1},{s2}]"

def reduce(s: str) -> str:
    """Returns a fully reduced snailfish number."""

    while True:
        attempt = explode(s)
        if attempt != "":
            s = attempt
            continue
        attempt = split(s)
        if attempt != "":
            s = attempt
            continue
        break
    return s

def magnitude(s: str) -> int:
    """Returns the magnitude of a snailfish number."""

    def mag(l: list) -> int:
        if type(l) == int:
            return l
        else:
            return 3 * mag(l[0]) + 2 * mag(l[1])

    return mag(eval(s))

def homework(data: str) -> int:
    """Returns the magnitude of a snailfish homework assignment."""
    lines = data.split()
    sum = reduce(lines[0])
    for sn in lines[1:]:
        sum = reduce(add(sum, sn))
    return magnitude(sum)

def max_pair_sum(data: str) -> int:
    """Returns the maximum magnitude of the sums of pairs of snailfish numbers."""
    lines = data.split()
    return max(magnitude(reduce(add(a,b)))
               for a in lines
               for b in lines
               if a is not b)


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    return homework(input_data)


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    return max_pair_sum(input_data)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=18)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
