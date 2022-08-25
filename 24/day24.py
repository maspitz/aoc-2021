"""Solves day 24, Advent of Code 2021."""

from aocd.models import Puzzle
import parse

"""The puzzle input is highly constrained, taking the form of 18 repeated
groups of 14 ALU instructions, as in:"""

PATTERN = """inp w
mul x 0
add x z
mod x 26
div z {I:d}
add x {A:d}
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y {B:d}
mul y x
add z y"""


"""Call a group of 18 such instructions one 'operation'.

The only register state retained from one operation to the next
is register z (because of the 'mul x 0' and 'mul y 0' instructions).

It is also register z that must have value 0 at the very end.

The parameter I takes the value 1 or 26.  Designate the
operations by this parameter.  The operations also has parameters A and B.

Let the operation be the nth operation, so that the inp w
gives the w register the nth digit of the input, d_n.

Let z0 designate the contents of the z register at the
beginning of the operation, and zn the contents at the end.

The 'eql' instructions effectively test whether d_n == z0 % 26 + A.
If the equality does not hold, then the y register will have the value d_n + B
at the end of the operation (due to 'mul y x')

But looking carefully at the puzzle input, we always have A > 9 for any
I=1 operations.  So the equality can never hold, and the result of any I=1 operation
is always that zn = 26 * z0 + (d_n + B).

If we consider zn represented in base-26, then I=1 operations
always effectively append one base-26 digit equal to (d_n + B).

As for I=26 operations:
if the equality does not hold, than zn = 26 * (z0 // 26) + (d_n + B), [*]
and if it does hold, then zn = (z0 // 26).  [**]

In the case of [*], then the last base-26 digit is replaced by (d_n + B).
In the case of [**], then the number is truncated by removed the last base-26 digit.

But notice: each I=1 operation appends a nonzero digit.  And in fact the numbers
of I=26 and I=1 operations are the same.  So we can only achieve z=0 at the finish
if every digit appended is removed during some I=26 operation.

So the equality must hold in every I=26 operation.  That is: d_n == z0 % 26 + A.
But z0 % 26 is the rightmost digit of the base-26 number, which was appended in
some previous I=1 operation.

In other words, the digits of the base-26 number form a stack.  Any I=1 operation
pushes the number (d_i + B_i) where i indexes this I=1 operation in our list.
For an I=26 operation to remove this digit from the stack, it must have
d_j == (d_i + B_i) + A_j, where j indexes the I=26 operation.

Because there are 7 I=1 and 7 I=26 operations, we have 7 constraints linking the
corresponding input digits.  Each constraint gives the difference between a pair
of digits in the model number.  In order to maximize (or minimize) the model number,
we must always make the leftmost of the pair of digits as great (or small) as possible
subject to its constraint.  This dictates the value of the other digit of the pair.

Thus, we can solve the problem by iterating through the 14 operations, maintaining
a stack of the B parameters and the corresponding input digit's place, and setting
the input digit values as this information is removed from the stack."""


def parse_input(input_data: str) -> list:
    """Parse the input data, returning a list of operations.

    Raises an error if our specific assumptions are not met."""

    results = [r.named for r in parse.findall(PATTERN, p.input_data)]
    pattern_lines = len(PATTERN.split('\n'))
    input_lines = len(p.input_data.split('\n'))
    
    if input_lines != pattern_lines * len(results):
        raise ValueError("The input did not match the expected pattern.")

    if any(r["I"] == 1 and r["A"] < 10 for r in results):
        raise ValueError("Parameter A is less than 10 in a type 1 operation.")

    if any(r["I"] not in {1, 26} for r in results):
        raise ValueError("Parameter I is not 1 or 26 in some operation.")

    type_1 = sum([r["I"] == 1 for r in results])
    type_26 = sum([r["I"] == 26 for r in results])
    if type_1 != type_26:
        raise ValueError("Unequal numbers of types 1 and 26 operations.")

    return results

def extremize_model(operations: list, maximize: bool) -> int:
    digits_list = [0] * len(operations)
    stack = []
    digit = 0
    for op in operations:
        if op["I"] == 1:
            stack.append((digit, op["B"]))
        else:
            other_digit, B_val = stack.pop()
            digit_difference = op["A"] + B_val
            ### constraint: THIS_DIGIT = OTHER_DIGIT + digit_difference
            if abs(digit_difference) > 8:
                raise ValueError("Digit difference constraint cannot be satisfied.")
            if maximize:
                digits_list[other_digit] = 9 - max(0, digit_difference)
            else:
                digits_list[other_digit] = 1 - min(0, digit_difference)
            digits_list[digit] = digits_list[other_digit] + digit_difference        
        digit += 1
    return int(''.join([str(d) for d in digits_list]))


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    ops = parse_input(input_data)
    return extremize_model(ops, maximize=True)


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""
    ops = parse_input(input_data)
    return extremize_model(ops, maximize=False)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=24)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
