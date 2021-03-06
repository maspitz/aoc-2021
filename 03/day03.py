"""Solves adventofcode.com/2021/day/3"""
import numpy as np

from aocd.models import Puzzle


def most_common_bits(bit_array: np.array) -> np.array:
    """Yields a bit vector containing the most common bits of a bit array.

    Given a (m x n) bit array, yields a (1 x n) bit array.
    If 0 and 1 are equally common at a position, then 1 is yielded."""

    bit_sums = np.sum(bit_array, axis=0)
    n_rows = np.size(bit_array, axis=0)
    return np.array(bit_sums / n_rows >= 0.5, dtype=int)


def bit_vector_to_int(bit_vector: np.array) -> int:
    """Converts a (1 x n) array of bits to an int."""

    bitvec_str = np.array2string(bit_vector, separator='')[1:-1]
    return int(bitvec_str, base=2)


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    # split input into list of lists, then convert to np.array
    bit_lists = [[bit for bit in line] for line in input_data.split()]
    bit_array = np.array(bit_lists, dtype=int)


    mcb = most_common_bits(bit_array)
    # lcb: least common bits
    lcb = 1 - mcb
    gamma = bit_vector_to_int(mcb)
    epsilon = bit_vector_to_int(lcb)

    return gamma * epsilon


def filter_by_bit_criteria(data: np.array, bit_number: int, criteria: int) -> np.array:
    """Return filtered data.

    If criteria=1, keep only rows having the most common
    value at the given bit_number.  For criteria=0,
    keep rows with least common value at bit_number.
    See puzzle instructions for details."""

    pass



def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    # split input into list of lists, then convert to np.array
    bit_lists = [[bit for bit in line] for line in input_data.split()]
    bit_array = np.array(bit_lists, dtype=int)


    # these refer to the same object, but this is OK since it won't be mutated
    oxy = bit_array
    co2 = bit_array

    # for each bit, in order, filter the rows of the oxy (co2) arrays
    # based on most (least) common bits remaining.
    for bit_idx in range(np.size(bit_array, 1)):
        if np.size(oxy, 0) > 1:
            oxy_mcb = most_common_bits(oxy)
            oxy = oxy[oxy[:, bit_idx] == oxy_mcb[bit_idx]]
        if np.size(co2, 0) > 1:
            co2_lcb = 1 - most_common_bits(co2)
            co2 = co2[co2[:, bit_idx] == co2_lcb[bit_idx]]

    if np.size(oxy, 0) != 1:
        raise ValueError("Oxygen generator rating is not unique")
    if np.size(co2, 0) != 1:
        raise ValueError("CO2 generator rating is not unique")

    oxy_rating = bit_vector_to_int(oxy[0,:])
    co2_rating = bit_vector_to_int(co2[0,:])

    return oxy_rating * co2_rating


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=3)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
