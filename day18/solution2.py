from collections import defaultdict
from itertools import count
from sys import stdin
import sys

data = stdin.read().strip().split('\n')

points: list[tuple[int, int]] = [tuple(int(a) for a in row.split(',')) for row in data]


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


def a_star(nodes: list[Node], start: Node, stop: Node):
    h = dict()
    g = dict()
    f = lambda node: h[node] + g[node]
    pred = dict()
    open = [start]
    closed = list()
    for node in nodes:
        h[node] = sum(abs(a - b) for a, b in zip(node.position, stop.position))
        g[node] = float("inf")
    g[start] = 0
    while len(open) > 0:
        node = sorted(open, key=f)[0]
        for connection in node.connections:
            other_node = connection.get_other(node)
            cost = connection.cost
            if g[other_node] > g[node] + cost:
                g[other_node] = g[node] + cost
                pred[other_node] = node
            if other_node not in open and other_node not in closed:
                open.append(other_node)
        open.remove(node)
        closed.append(node)
    res = []
    node = stop
    while (prev := pred.get(node)) is not None:
        res.append(node)
        node = prev
    res.reverse()
    return [start] + res

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


SIZE = 71
def try_do_step(pre_steps: int):
    board = [["." for _ in range(SIZE)] for _ in range(SIZE)]
    grid = defaultdict(lambda: {})
    for y in range(SIZE):
        for x in range(SIZE):
            new_node = Node(x, y)
            grid[x][y] = new_node
            node_above = grid[x - 1].get(y)
            if node_above is not None:
                Connection(new_node, node_above)
            node_left = grid[x].get(y - 1)
            if node_left is not None:
                Connection(new_node, node_left)

    current_pos = 0, 0
    goal_node = grid[SIZE - 1][SIZE - 1]
    assert goal_node is not None

    points_iter = iter(points)

    for _, (falling_x, falling_y) in zip(range(pre_steps), points_iter):
        node = grid[falling_x][falling_y]
        node.destroy()
        grid[falling_x][falling_y] = None
        board[falling_x][falling_y] = "#"

    nodes = []
    for row in grid.values():
        for n in row.values():
            if n is not None:
                nodes.append(n)
    current_x, current_y = current_pos
    current_node = grid[current_x][current_y]
    path = a_star(nodes, current_node, goal_node)
    if len(path) == 1:
        return None
    return len(path) - 1

for i in count():
    res = try_do_step(i)
    print(i, res)
    if res is None:
        print(points[i - 1])
        break
