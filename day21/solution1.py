from collections import defaultdict
from sys import stdin
from itertools import pairwise

codes_to_type = stdin.read().strip().split('\n')

up = "^"
down = "v"
left = "<"
right = ">"


keypad_map = {
    up: {
            up: ['A'],
            down: ['vA'],
            left: ['v<A'],
            right: ['v>A', '>vA'],
            'A': ['>A']
        },
    down: {
            up: ['^A'],
            down: ['A'],
            left: ['<A'],
            right: ['>A'],
            'A': ['>^A', '^>A']
        },
    left: {
            up: ['>^A'],
            down: ['>A'],
            left: ['A'],
            right: ['>>A'],
            'A': ['>>^A']
        },
    right: {
            up: ['^<A', '<^A'],
            down: ['<A'],
            left: ['<<A'],
            right: ['A'],
            'A': ['^A']
        },
    'A': {
            up: ['<A'],
            down: ['<vA', 'v<A'],
            left: ['v<<A'],
            right: ['vA'],
            'A': ['A']
        },
    }

def walk_sequences(s: list[tuple[str, str]]):
    source, destination = s[0]
    
    seq = keypad_map[source][destination]
    for sub_seq in seq:
        if len(s) == 1:
            yield sub_seq
        else:
            yield from (sub_seq + sub_sub_seq for sub_sub_seq in walk_sequences(s[1:]))

def do_keypad_sequences(root: str, depth = 0):
    pairs = list(pairwise(['A', *root]))
    sequences = walk_sequences(pairs)
    if depth < 2:
        for s in sequences:
            yield from do_keypad_sequences(s, depth + 1)
    else:
        yield from sequences

door_keypad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", 'A']
]



class Connection:
    def __init__(self, node1, node2, cost):
        self.nodes = (node1, node2)
        self.cost = cost
        for node in self.nodes:
            node.connections.append(self)

    def get_other(self, first):
        if self.nodes[0] is first:
            return self.nodes[1]
        else:
            return self.nodes[0]
    
    def __repr__(self):
        return f"{self.nodes[0].position} <-{self.cost}-> {self.nodes[1].position}"

class Node:
    def __init__(self, y, x):
        self.position = y, x
        self.connections: list[Connection] = []

    def __repr__(self):
        return f"Node: {self.position=}"

    def get_others(self):
        return [x.get_other(self) for x in self.connections]

    def get_connection(self, other) -> Connection | None:
        for connection in self.connections:
            if connection.get_other(self) is other:
                return connection
        else:
            return None

grid: dict[tuple[int, int], Node] = {}
key_to_node: dict[str, Node] = {}
nodes: list[Node] = []

for y, row in enumerate(door_keypad):
    for x, key in enumerate(row):
        if key is None:
            continue
        node = Node(y, x)
        grid[y, x] = node
        key_to_node[key] = node
        nodes.append(node)

connections = []
d_up = lambda x, y: (x-1, y)
d_down = lambda x, y: (x+1, y)
d_left = lambda x, y: (x, y-1)
d_right = lambda x, y: (x, y+1)

directions = {
    up: d_up,
    down: d_down,
    left: d_left,
    right: d_right
}

for node in nodes:
    for d in [d_left, d_up]:
        next_node_pos = d(*node.position)
        next_node = grid.get(next_node_pos)
        if next_node is None:
            continue
        Connection(node, next_node, 1)

def walk_pred(start, end: Node, pred: dict[Node, list[Node]]):
    result = []
    node = end
    while True:
        prev = pred.get(node)
        if prev is None:
            yield [*reversed(result)]
            break
        if len(prev) == 1:
            result.append(prev[0])
            node = prev[0]
        else:
            for c in prev:
                for path in walk_pred(start, c, pred):
                    a_path = [*path, c, *reversed(result)]
                    yield a_path
            break


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
                pred[other_node] = [node]
            elif g[other_node] == g[node] + cost:
                pred[other_node].append(node)
            if other_node not in open and other_node not in closed:
                open.append(other_node)
        open.remove(node)
        closed.append(node)
    return walk_pred(start, stop, pred)

def node_path_to_moves(nodes: list[Node]):
    acc = ""
    for a, b in pairwise(nodes):
        for char, f in directions.items():
            if f(*a.position) == b.position:
                acc += char
                break
        else:
            raise Exception(a, b)
    return acc


def path_for_code(code: str):
    key_nodes = [key_to_node[l] for l in ["A", *code]]
    paths = []
    for source, destination in pairwise(key_nodes):
        new_paths = list([[*p, destination] for p in a_star(nodes, source, destination)])
        paths.append(new_paths)
    paths1, paths2, paths3, paths4 = [[node_path_to_moves(s_p) for s_p in p] for p in paths]

    for p1 in paths1:
        for p2 in paths2:
            for p3 in paths3:
                for p4 in paths4:
                    yield "A".join([p1, p2, p3, p4]) + "A"

    
    
acc = 0

for code in codes_to_type:
    paths = list(path_for_code(code))
    expansions = sum((list(do_keypad_sequences(sequence)) for sequence in paths), start=[])
    min_length = min(len(s) for s in expansions)
    print(code, min_length)
    complexity = int(code.strip('A'))
    acc += complexity * min_length

print(acc)


"""
assert "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A" in expansions
"""
