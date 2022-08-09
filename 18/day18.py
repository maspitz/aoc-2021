"""Solves day 18, Advent of Code 2021."""

from aocd.models import Puzzle

MAX_DEPTH = 5
MAX_NODES = 2**(MAX_DEPTH+1) - 1

class Snailfish:
    """Class for snailfish number."""

    def __init__(self, s: str):
        """Sets the snailfish values from a string representation."""
        self.data = [None] * MAX_NODES
        if s != None:
            self._set_from_list(0, eval(s))

    def _set_from_list(self, i: int, val: any):
        # sets the subtree at node i.  val is list or int.
        if type(val) == list:
            self.data[i] = None
            self._set_from_list(self.left(i), val[0])
            self._set_from_list(self.right(i), val[1])
        else:
            self.data[i] = val

    def __str__(self) -> str:
        return self._to_str(0)
        
    def _to_str(self, i) -> str:
        # convert the subtree at i to string
        if self.data[i] == None:
            return ("[" + self._to_str(self.left(i)) + ","
                    + self._to_str(self.right(i)) + "]")
        else:
            return str(self.data[i])
        
    def __repr__(self) -> str:
        return f"Snailfish('{self.__str__()}')"
            
    def is_leaf(self, i: int) -> bool:
        """Returns True if node i is a leaf"""
        return self.data[i] != None

    def left(self, i: int) -> int:
        """Returns the index of the left child of node i."""
        return i * 2 + 1

    def right(self, i: int) -> int:
        """Returns the index of the right child of node i."""
        return i * 2 + 2

    def parent(self, i: int) -> int:
        """Returns the index of the parent of node i, or None if root."""
        if i == 0:
            return None
        return (i - 1) // 2
    
    def find_max_depth(self) -> int:
        """Return the index of leftmost leaf at MAX_DEPTH, or None if none."""

        for i in range(MAX_NODES // 2, MAX_NODES):
            if self.data[i] != None:
                return i
        return None

    def explode(self) -> bool:
        """Explodes the snailfish number.  Returns False if no explosion."""

        i = self.find_max_depth()
        if i is None:
            return False
        left_idx, right_idx = i, i + 1
        parent_idx = i // 2
        left_number = self.data[left_idx]
        right_number = self.data[right_idx]
        self.data[left_idx] = None
        self.data[right_idx] = None
        self.data[parent_idx] = 0
        idx_to_left = self.find_number_to_left(parent_idx)
        idx_to_right = self.find_number_to_right(parent_idx)
        if idx_to_left is not None:
            self.data[idx_to_left] += left_number
        if idx_to_right is not None:
            self.data[idx_to_right] += right_number
        return True

    def find_number_to_left(self, idx: int) -> int:
        """Return index of first regular number to left of idx; otherwise, None."""
        while idx != 0 and idx % 2 == 1:
            idx = self.parent(idx)
        if idx == 0:
            return None
        idx = self.left(self.parent(idx))
        while not self.is_leaf(idx):
            idx = self.right(idx)
        return idx

    def find_number_to_right(self, idx: int) -> int:
        """Return index of first regular number to right of idx; otherwise, None."""
        while idx != 0 and idx % 2 == 0:
            idx = self.parent(idx)
        if idx == 0:
            return None
        idx = self.right(self.parent(idx))
        while not self.is_leaf(idx):
            idx = self.left(idx)
        return idx
    
    def find_splittable(self) -> int:
        """Return the index of the leftmost number >= 10.  None if none"""
        node_stack = [0]
        while len(node_stack) > 0:
            i = node_stack.pop()
            if self.is_leaf(i):
                if self.data[i] >= 10:
                    return i
                continue
            else:
                node_stack.append(self.right(i))
                node_stack.append(self.left(i))
        return None
    
    def split(self) -> bool:
        """Splits the snailfish number.  Returns False if no split."""
        i = self.find_splittable()
        if i is None:
            return False
        val = self.data[i]
        self.data[i] = None
        self.data[self.left(i)] = val // 2
        self.data[self.right(i)] = val // 2 + val % 2
        return True

    def reduce(self):
        """Reduces the snailfish number by exploding and splitting."""

        while True:
            if self.explode() == True:
                continue
            elif self.split() == True:
                continue
            else:
                break


    def magnitude(self, idx=0) -> int:
        """Returns the magnitude of the snailfish number."""
        if self.is_leaf(idx):
            return self.data[idx]
        return (3 * self.magnitude(self.left(idx)) +
                2 * self.magnitude(self.right(idx)))
        
    def add(self, b: "Snailfish") -> "Snailfish":
        """Reduces self and b and returns their sum as a new reduced snailfish number."""

        a = self
        a.reduce()
        b.reduce()
        c = Snailfish(None)
        offset_a = 1
        offset_b = 2
        start, stop = 0, 0
        start_a, stop_a = 1, 1
        start_b, stop_b = 2, 2
        for depth in range(0, MAX_DEPTH):
            c.data[start_a:stop_a+1] = a.data[start:stop+1]
            c.data[start_b:stop_b+1] = b.data[start:stop+1]
            start, stop = c.left(start), c.right(stop)
            start_a, stop_a = a.left(start_a), a.right(stop_a)
            start_b, stop_b = b.left(start_b), b.right(stop_b)
        c.reduce()
        return c
        

def snailfish_sum(snlist: list) -> Snailfish:
    """Returns the sum of a list of snailfish numbers."""
    total = snlist[0]
    for sn in snlist[1:]:
        total = total.add(sn)
    return total


def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""
    sn_list = [Snailfish(s) for s in input_data.split()]
    return snailfish_sum(sn_list).magnitude()


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""
    sn_list = [Snailfish(s) for s in input_data.split()]
    n = len(sn_list)
    return max(sn_list[i].add(sn_list[j]).magnitude()
               for i in range(n)
               for j in range(n)
               if i != j)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=18)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
