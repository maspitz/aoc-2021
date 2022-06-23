import day01

test_input_data = """199
200
208
210
200
207
240
269
260
263"""


def test_part_a():
    "Test the solution on sample data for part A."
    assert day01.part_a(test_input_data) == 7


def test_part_b():
    "Test the solution on sample data for part B."
    assert day01.part_b(test_input_data) == 5
