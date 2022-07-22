"""Tests for day 16 of Advent of Code 2021."""

import day16

def test_version_sums():
    """Test packet version sums."""

    sample_inputs = ["8A004A801A8002F478", "620080001611562C8802118E34", "C0015000016115A2E0802F182340", "A0016C880162017C3686B18A3D4780"]

    sample_version_sums = [16, 12, 23, 31]

    for test_input, test_sum in zip(sample_inputs, sample_version_sums):
        assert day16.part_a(test_input) == test_sum


def test_sum_operation():
    """Test: C200B40A82 finds the sum of 1 and 2, resulting in the value 3."""

    p = day16.Packet(day16.parse_input('C200B40A82'))
    assert(len(p.subpackets) == 2)
    assert(p.subpackets[0].value == 1)
    assert(p.subpackets[1].value == 2)
    assert(p.value == 3)

def test_prod_operation():
    """04005AC33890 finds the product of 6 and 9, resulting in the value 54."""
    p = day16.Packet(day16.parse_input('04005AC33890'))
    assert(len(p.subpackets) == 2)
    assert(p.subpackets[0].value == 6)
    assert(p.subpackets[1].value == 9)
    assert(p.value == 54)

def test_min_operation():
    """880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7."""
    p = day16.Packet(day16.parse_input('880086C3E88112'))
    assert(len(p.subpackets) == 3)
    assert(p.subpackets[0].value == 7)
    assert(p.subpackets[1].value == 8)
    assert(p.subpackets[2].value == 9)
    assert(p.value == 7)

def test_max_operation():
    """CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9."""
    p = day16.Packet(day16.parse_input('CE00C43D881120'))
    assert(len(p.subpackets) == 3)
    assert(p.subpackets[0].value == 7)
    assert(p.subpackets[1].value == 8)
    assert(p.subpackets[2].value == 9)
    assert(p.value == 9)

def test_lt_operation():
    """D8005AC2A8F0 produces 1, because 5 is less than 15."""
    p = day16.Packet(day16.parse_input('D8005AC2A8F0'))
    assert(len(p.subpackets) >= 2)
    assert(p.subpackets[0].value == 5)
    assert(p.subpackets[1].value == 15)
    assert(p.value == 1)

def test_gt_operation():
    """F600BC2D8F produces 0, because 5 is not greater than 15."""
    p = day16.Packet(day16.parse_input('F600BC2D8F'))
    assert(len(p.subpackets) >= 2)
    assert(p.subpackets[0].value == 5)
    assert(p.subpackets[1].value == 15)
    assert(p.value == 0)

def test_eq_operation():
    """9C005AC2F8F0 produces 0, because 5 is not equal to 15."""
    p = day16.Packet(day16.parse_input('9C005AC2F8F0'))
    assert(len(p.subpackets) >= 2)
    assert(p.subpackets[0].value == 5)
    assert(p.subpackets[1].value == 15)
    assert(p.value == 0)
    
def test_compound_operation():
    """9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2."""
    p = day16.Packet(day16.parse_input('9C0141080250320F1802104A08'))
    assert(len(p.subpackets) == 2)
    assert(p.subpackets[0].value == 4)
    assert(p.subpackets[1].value == 4)
    assert(p.value == 1)

