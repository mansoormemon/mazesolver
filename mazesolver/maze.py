import numpy as np


N, S, E, W = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPPOSITE = {E: W, W: E, N: S, S: N}


class Node:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent


class DisjointSet:
    def __init__(self, nodes):
        self.node_map = {}

        for i, value in enumerate(nodes):
            n = Node(value, i)
            self.node_map[value] = n

    def find_parent(self, node):
        return self.find_node(node).parent

    def find_node(self, node):
        if type(self.node_map[node].parent) is int:
            return self.node_map[node]
        else:
            parent_node = self.find_node(self.node_map[node].parent.value)
            self.node_map[node].parent = parent_node
            return parent_node

    def union(self, node_a, node_b):
        parent_a = self.find_node(node_a)
        parent_b = self.find_node(node_b)
        if parent_a.parent != parent_b.parent:
            parent_a.parent = parent_b


class Maze:
    @staticmethod
    def generate(grid_shape, seed):
        def neighbor(r, c, direction):
            return r + DY[direction], c + DX[direction]

        def compute_maze_shape(rows, cols):
            return rows * 2 + 1, cols * 2 + 1

        np.random.seed(seed)

        rows, cols = grid_shape

        nodes = [(r, c) for r in range(int(rows)) for c in range(int(cols))]

        disjoint_set = DisjointSet(nodes)

        internal_edges = []
        for r, c in nodes:
            if r:
                internal_edges.append((neighbor(r, c, N), (r, c)))
            if c:
                internal_edges.append((neighbor(r, c, W), (r, c)))

        maze = []
        for edge in sorted(internal_edges, key=lambda _: np.random.random()):
            node_a, node_b = edge
            if disjoint_set.find_parent(node_a) != disjoint_set.find_parent(node_b):
                disjoint_set.union(node_a, node_b)
                maze.append(edge)

        maze_shape = compute_maze_shape(rows, cols)
        maze_map = np.zeros(maze_shape, dtype=np.uint8)
        for edge in maze:
            (a_r, a_c), (b_r, b_c) = edge
            min_x, min_y = compute_maze_shape(min(a_r, b_r), min(a_c, b_c))
            max_x, max_y = compute_maze_shape(max(a_r, b_r), max(a_c, b_c))
            maze_map[min_x : max_x + 1, min_y : max_y + 1] = 1

        return maze_map

    @staticmethod
    def solve(maze):
        rows, cols = maze.shape

        def is_in_bounds(x, y):
            return (
                x >= 0 and x < cols - 1 and y >= 0 and y < rows - 1 and maze[y][x] == 1
            )

        def attemt_solve(maze, x, y, sol):
            if x == cols - 2 and y == 1:
                sol[y][x] = 1
                return True

            if is_in_bounds(x, y):
                if sol[y][x] == 1:
                    return False

                sol[y][x] = 1
                if attemt_solve(maze, x + DX[E], y, sol):
                    return True

                if attemt_solve(maze, x, y + DY[S], sol):
                    return True

                if attemt_solve(maze, x + DX[W], y, sol):
                    return True

                if attemt_solve(maze, x, y + DY[N], sol):
                    return True

                sol[y][x] = 0
                return False

        path = np.zeros_like(maze)
        if not attemt_solve(maze, 1, rows - 2, path):
            return False

        vf_path = path[::-1]

        return vf_path
