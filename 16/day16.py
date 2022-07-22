"""Solves day 16, Advent of Code 2021."""

from aocd.models import Puzzle
from math import prod

def parse_input(input_data: str) -> tuple:
    """Given a hex string, return a tuple of bits."""
    hex_to_nibbles = {digit: f"{int(digit, 16):04b}"
                   for digit in "0123456789ABCDEF"}
    nibbles = [hex_to_nibbles[ch] for ch in input_data]
    bits = tuple(int(bit)
                 for x in nibbles
                 for bit in x)
    return bits


def parse_binary(bits: tuple) -> int:
    """Convert a tuple of bits to an integer value."""
    
    n = 0
    for bit in bits:
        n *= 2
        n += bit
    return n


class Packet:
    """Interprets a tuple of bits as a packet."""
    
    def __init__(self, data: tuple):
        """Initializes the packet with a tuple of bits.

        All subpackets are created and initialized as well.
        """
        self.data = data
        self.subpackets = []
        self.value, self.length = self.find_value_and_length()

    def find_value_and_length(self) -> (int, int):
        """Find this packet's value and total length, depending on type ID."""

        if self.type_ID == 4:
            return self.__literal_value_and_length()
        else:
            return self.__operator_value_and_length()

    @property
    def version(self) -> int:
        """Packet version number"""
        return parse_binary(self.data[0:3])

    @property
    def type_ID(self) -> int:
        """Packet type ID"""
        return parse_binary(self.data[3:6])
    
    def __literal_value_and_length(self) -> (int, int):
        """Return value and length for literal value type packet."""

        group_index = 6
        value = 0
        while True:
            value <<= 4
            value += parse_binary(self.data[group_index+1:group_index+5])
            if self.data[group_index] == 0:
                return value, group_index + 5
            group_index += 5

    def __operator_value_and_length(self) -> (int, int):
        """Return value and length for operator type packet."""

        def append_next_subpacket(idx):
            """Read and append subpacket at idx."""
            p = Packet(self.data[idx:])
            self.subpackets.append(p)

        length = None
        length_type_ID = self.data[6]
        if length_type_ID == 0:
            idx = 22
            total_subpacket_length = parse_binary(self.data[7:22])
            length = idx + total_subpacket_length
            while idx < length:
                append_next_subpacket(idx)
                idx += self.subpackets[-1].length
                
        elif length_type_ID == 1:
            idx = 18
            total_subpacket_number = parse_binary(self.data[7:18])
            for j in range(total_subpacket_number):
                append_next_subpacket(idx)
                idx += self.subpackets[-1].length
            length = idx

        value = self.__evaluate_operator()
        return value, length

    def __evaluate_operator(self) -> int:
        """Evaluate operator packet applied to subpacket values."""
        
        id = self.type_ID
        sp_values = [sp.value for sp in self.subpackets]
        if id == 0: return sum(sp_values)
        if id == 1: return prod(sp_values)
        if id == 2: return min(sp_values)
        if id == 3: return max(sp_values)
        if id == 5: return int(sp_values[0] > sp_values[1])
        if id == 6: return int(sp_values[0] < sp_values[1])
        if id == 7: return int(sp_values[0] == sp_values[1])
            

def packet_version_sum(p: Packet):
    """Sums the version numbers of the packet and subpackets."""
    return p.version + sum([packet_version_sum(sp) for sp in p.subpackets])


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    p = Packet(parse_input(input_data))
    return packet_version_sum(p)


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    p = Packet(parse_input(input_data))
    return p.value


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=16)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
