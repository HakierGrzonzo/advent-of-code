from collections import defaultdict
from itertools import count
from sys import stdin
from multiprocessing import pool
import sys

raw_board = stdin.read().strip()


up = lambda x, y: (x-1, y)
up.__str__ = lambda: "|"
down = lambda x, y: (x+1, y)
down.__str__ = lambda: "|"
left = lambda x, y: (x, y-1)
left.__str__ = lambda: "-"
right = lambda x, y: (x, y+1)
right.__str__ = lambda: "-"


class Connection:
    def __init__(self, node1, node2):
        self.nodes = (node1, node2)
        self.cost = 1
        for node in self.nodes:
            node.connections.append(self)

    def get_other(self, first) -> 'Node':
        if self.nodes[0] is first:
            return self.nodes[1]
        else:
            return self.nodes[0]
    
    def __repr__(self):
        return f"{self.nodes[0].position} <-{self.cost}-> {self.nodes[1].position}"

class Node:
    def __init__(self, x, y):
        self.position = x, y
        self.connections: list[Connection] = []
        self.is_valid = True

    def __repr__(self):
        return f"Node: {self.position=}"

    def get_others(self):
        return [x.get_other(self) for x in self.connections]

    def destroy(self):
        for connection in self.connections:
            other = connection.get_other(self)
            other.connections = [c for c in other.connections if c is not connection]
        self.is_valid = False

    def get_connection(self, other) -> Connection | None:
        for connection in self.connections:
            if connection.get_other(self) is other:
                return connection
        else:
            return None

def dijkstra(start: Node, nodes: list[Node]):
    nodes = nodes.copy()
    pred = dict()
    k = dict()
    for node in nodes:
        pred[node] = None
        k[node] = float('inf')
    k[start] = 0
    while len(nodes) > 0:
        node = min(nodes, key=lambda item: k[item])
        nodes.remove(node)
        for connection in node.connections:
            other_node = connection.get_other(node)
            if other_node in nodes:
                if k[other_node] > connection.cost + k[node]:
                    k[other_node] = connection.cost + k[node]
                    pred[other_node] = node
    return k

def debug_graph(nodes: list[Node]):
    file = open('/tmp/debug.dot', 'w+')
    file.write("digraph G {")
    for node in nodes:
        x, y = node.position
        file.write(f"node{x}A{y} [label=\"{str(node.position)}\"];\n")
        for connection in node.connections:
            other = connection.get_other(node)
            other_x, other_y = other.position
            file.write(f"node{x}A{y} -> node{other_x}A{other_y};\n")

    file.write("}")
    sys.exit(1)

grid: dict[int, dict[int, Node]] = defaultdict(lambda: {})
normal_nodes: list[Node] = []
wall_nodes: list[Node] = []

start = -1, -1 
goal = -1, -1 

for y, row in enumerate(raw_board.split('\n')):
    for x, char in enumerate(row):
        node = Node(y, x)
        if char == "#":
            wall_nodes.append(node)
            continue
        if char == "S":
            start = y, x
        elif char == "E":
            goal = y, x
        grid[y][x] = node
        normal_nodes.append(node)

start_y, start_x = start
start_node = grid[start_y][start_x]
goal_y, goal_x = goal
goal_node = grid[goal_y][goal_x]

for y, row in grid.items():
    for x, node in row.items():
        for direction in [left, up]:
            next_y, next_x = direction(y, x)
            next_node = grid.get(next_y, {}).get(next_x)
            if next_node is None:
                continue
            Connection(node, next_node)


def get_possible_shortcuts():
    for wall_node in wall_nodes:
        directions = [(left, [up, down, right]), (up, [down, right])]
        for dir_a, dirs in directions:
            a_y, a_x = dir_a(*wall_node.position)
            a_node = grid.get(a_y, {}).get(a_x)
            if a_node is None:
                continue
            for dir_b in dirs:
                b_y, b_x = dir_b(*wall_node.position)
                b_node = grid.get(b_y, {}).get(b_x)
                if b_node is None:
                    continue
                yield a_node, b_node
                yield b_node, a_node

print("part 1")
from_start = dijkstra(start_node, normal_nodes)
print("part 2")
from_goal = dijkstra(goal_node, normal_nodes)

shortest_path_length = from_start[goal_node]

print(f"{shortest_path_length=}")

shortcuts = defaultdict(lambda: 0)

num_of_paths = len(list(get_possible_shortcuts()))

print(f"Count to evaluate {num_of_paths}")

cache = defaultdict(lambda: {})

for i, (a_node, b_node) in enumerate(get_possible_shortcuts()):
    first_path = from_start.get(a_node)
    second_path = from_goal.get(b_node)
    if first_path is None or second_path is None:
        continue
    total_length = first_path + second_path + 2
    shortcuts[total_length] += 1

acc = 0
for value, count in sorted(shortcuts.items(), key=lambda i: i[0]):
    saved = shortest_path_length - value
    print(f"{saved=}:\t{count}")
    if saved >= 100:
        acc += count

print(acc)

