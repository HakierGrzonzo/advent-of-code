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

def dijkstra(start: Node, nodes: list[Node], max_depth = None) -> dict[Node, int]:
    nodes = nodes.copy()
    k = dict()
    for node in nodes:
        k[node] = float('inf')
    k[start] = 0
    while len(nodes) > 0:
        node = min(nodes, key=lambda item: k[item])
        nodes.remove(node)
        if max_depth is not None and k[node] > max_depth:
            break
        for connection in node.connections:
            other_node = connection.get_other(node)
            if other_node in nodes:
                if k[other_node] > connection.cost + k[node]:
                    k[other_node] = connection.cost + k[node]
    return k

grid: dict[int, dict[int, Node]] = defaultdict(lambda: {})
normal_nodes: list[Node] = []

start = -1, -1 
goal = -1, -1 

for y, row in enumerate(raw_board.split('\n')):
    for x, char in enumerate(row):
        node = Node(y, x)
        if char == "#":
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

def connect(this_grid: dict[int, dict[int, Node]]):
    for y, row in this_grid.items():
        for x, node in row.items():
            for direction in [left, up]:
                next_y, next_x = direction(y, x)
                next_node = this_grid.get(next_y, {}).get(next_x)
                if next_node is None:
                    continue
                Connection(node, next_node)

connect(grid)

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


print("part 1")
from_start = dijkstra(start_node, normal_nodes)
print("part 2")
from_goal = dijkstra(goal_node, normal_nodes)

shortest_path_length = from_start[goal_node]

print(f"{shortest_path_length=}")

shortcuts = defaultdict(lambda: 0)

cache = defaultdict(lambda: {})

def get_nodes_with_distance(position):
    y, x = position
    for node in normal_nodes:
        n_y, n_x = node.position
        distance = abs(n_y - y) + abs(n_x - x)
        if distance == 0 or distance > 20:
            continue
        yield node, distance

for node in normal_nodes:
    first_path = from_start[node]
    for b_node, shortcut_distance in get_nodes_with_distance(node.position):
        second_path = from_goal[b_node]
        total_length = first_path + second_path + shortcut_distance
        shortcuts[total_length] += 1

acc = 0
for value, count in sorted(shortcuts.items(), key=lambda i: -i[0]):
    saved = shortest_path_length - value
    if saved >= 50:
        print(f"{saved=}:\t{count}")
    if saved >= 100:
        acc += count

print(acc)

