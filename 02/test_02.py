import day02

test_input_data = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


def test_part_a():
    "Test the solution on sample data for part A."
    assert day02.part_a(test_input_data) == 150


def test_part_b():
    "Test the solution on sample data for part B."
    assert day02.part_b(test_input_data) == 900
