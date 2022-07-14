"""Solves day 12, Advent of Code 2021."""

from aocd.models import Puzzle


def make_graph(input_data: str) -> dict:
    """Return a graph corresponding to the cave map.

    The graph is represented by an adjacency list (dictionary).
    Nodes are keyed by the cave name string.
    Edges are bidirectional except for those emanating from start."""

    def assert_big_or_small(cave_name: str):
        if not (cave_name.isupper() or cave_name.islower()):
            raise ValueError(f"make_graph: {cave_name} is neither big nor small.")
    
    adj_list = dict()
    lines = input_data.split('\n')
    for line in lines:
        node1, node2 = line.split('-')
        adj_list.setdefault(node1, [])
        adj_list.setdefault(node2, [])
        if node2 != "start":
            adj_list[node1].append(node2)
        if node1 != "start":
            adj_list[node2].append(node1)
        if node1.isupper() and node2.isupper():
            raise ValueError(f"make_graph: {line} connects two big caves.")
        assert_big_or_small(node1)
        assert_big_or_small(node2)
    return adj_list


def count_cave_paths_a(graph: dict) -> int:
    """Counts the cave paths subject to part A constraints.

    Constraints:
    - Paths go from start to end.
    - Small caves are visited 0 or 1 times.
    - Big caves are visited any number of times."""

    is_small = str.islower

    def count_paths_dfs(path: list) -> int:
        total_paths = 0
        cur_node = path[-1]
        next_nodes = graph[cur_node]
        for node in next_nodes:
            if node == "end":
                total_paths += 1
            elif is_small(node) and node in path:
                continue
            else:
                path.append(node)
                total_paths += count_paths_dfs(path)
                path.pop()
        return total_paths
    
    return count_paths_dfs(["start"])
    
    

def part_a(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""

    g = make_graph(input_data)    
    return count_cave_paths_a(g)



def count_cave_paths_b(graph: dict) -> int:
    """Counts the cave paths subject to part B constraints.

    Constraints:
    - Paths go from start to end.
    - One small cave can me visited up to 2 times.
    - Other small caves are visited 0 or 1 times.
    - Big caves are visited any number of times."""

    is_small = str.islower

    def count_paths_dfs(path: list, double_cave = None) -> int:
        total_paths = 0
        cur_node = path[-1]
        next_nodes = graph[cur_node]
        for node in next_nodes:
            if node == "end":
                total_paths += 1
            elif is_small(node) and node in path:
                if double_cave is None:
                    path.append(node)
                    total_paths += count_paths_dfs(path, node)
                    path.pop()
                else:
                    continue
            else:
                path.append(node)
                total_paths += count_paths_dfs(path, double_cave)
                path.pop()
        return total_paths
    
    return count_paths_dfs(["start"])
    


def part_b(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part B."""

    g = make_graph(input_data)    
    return count_cave_paths_b(g)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=12)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    print(f"  Part A: {part_a(puzzle.input_data)}")
    print(f"  Part B: {part_b(puzzle.input_data)}")
