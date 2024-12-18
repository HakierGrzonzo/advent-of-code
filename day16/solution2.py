from collections import defaultdict
from sys import setrecursionlimit, stdin, exit
from itertools import pairwise

board = stdin.read().strip()


up = lambda x, y: (x-1, y)
up.__str__ = lambda: "|"
down = lambda x, y: (x+1, y)
down.__str__ = lambda: "|"
left = lambda x, y: (x, y-1)
left.__str__ = lambda: "-"
right = lambda x, y: (x, y+1)
right.__str__ = lambda: "-"

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
    def __init__(self, y, x, direction, meta=""):
        self.position = y, x
        self.direction = direction
        self.meta = meta
        self.connections: list[Connection] = []

    def __repr__(self):
        return f"Node: {self.position=} {self.direction}"

    def get_others(self):
        return [x.get_other(self) for x in self.connections]

    def get_connection(self, other) -> Connection | None:
        for connection in self.connections:
            if connection.get_other(self) is other:
                return connection
        else:
            return None

grid: dict[int, dict[int, tuple[Node, Node]]] = defaultdict(lambda: {})
nodes: list[Node] = []

def debug_graph(nodes: list[Node]):
    file = open('/tmp/debug.dot', 'w+')
    file.write("digraph G { overlap=\"prism\";")
    for node in nodes:
        x, y = node.position
        file.write(f"node{x}A{y} [label=\"{str(node.position)}\\n\"];\n")
        for connection in node.connections:
            other = connection.get_other(node)
            other_x, other_y = other.position
            file.write(f"node{x}A{y} -> node{other_x}A{other_y};\n")

    file.write("}")
    exit(1)
start = None, None
goal = None, None

for y, row in enumerate(board.split('\n')):
    for x, char in enumerate(row):
        if char == "#":
            continue
        if char == "S":
            start = y, x
        elif char == "E":
            goal = y, x
        node1 = Node(y, x, 'vertical', char)
        node2 = Node(y, x, 'horizontal', char)
        grid[y][x] = node1, node2
        nodes.append(node1)
        nodes.append(node2)

connections = []

def try_connect(node: Node, direction):
    y, x = direction(*node.position)
    next_node = grid.get(y, {}).get(x)
    if next_node is None:
        return
    nodeV, nodeH = next_node
    node_to_connect = nodeV if direction is up or direction is down else nodeH
    connections.append(Connection(node, node_to_connect, 1))


for y, row in grid.items():
    for x, (nodeV, nodeH) in row.items():
        connections.append(Connection(nodeV, nodeH, 1000))
        try_connect(nodeH, left)
        try_connect(nodeV, up)
            

setrecursionlimit(100_000)

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


start_y, start_x = start
start_node = grid[start_y][start_x]
goal_y, goal_x = goal
goal_node = grid[goal_y][goal_x]

def get_cost(path):
    #print(*path, sep="\n\t")
    cost_b = 1
    for a, b in pairwise(path):
        conn = a.get_connection(b)
        if conn is None:
            raise Exception(a, b, a.connections)
        y, x = b.position
        #board_str[y][x] = "@" if conn.cost > 1 else "*"
        cost_b += conn.cost
    return cost_b

def evaluate_paths(i):
    paths = a_star(nodes, start_node[1], goal_node[i])

    paths_and_costs = [(get_cost(path), path) for path in paths]
    m_cost = min(paths_and_costs, key=lambda n: n[0])[0]
    paths = [path for cost, path in paths_and_costs if cost == m_cost]
    return m_cost, paths

_, m_paths = min([evaluate_paths(i) for i in [0, 1]], key=lambda n: n[0])

visited_coords = set()
for path in m_paths:
    for node in path:
        visited_coords.add(node.position)
print(len(visited_coords) + 1)
