# from math import inf

from artifact.tagartifact import TagArtifact, TagType, TagSubType
from entity import Entity


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return not (self == other)


class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __hash__(self):
        return hash((self.u, self.v))

    def __eq__(self, other):
        return (self.u, self.v) == (other.u, other.v)

    def __ne__(self, other):
        return not (self == other)


class Pathfinder(Entity):
    def __init__(self, board):
        super(Pathfinder, self).__init__()
        self.board = board
        self.nodes = []
        self.shortestPaths = {}
        self.indexesNodes = {}
        self.nodesIndexes = []
        self.nextNodes = []
        self.addartifact(TagArtifact(TagType.OTHER, TagSubType.PATHFINDER))

    def prepareallstepsforshortestpaths(self):
        # Generate all edges of graph
        max_y = len(self.board)
        max_x = len(self.board[1])
        nodes_indexes = [[0 for x in range(max_y)] for y in range(max_x)]
        self.indexesNodes.clear()

        i = 0
        y = 0
        for row in self.board:
            x = 0
            for cell in row:
                if cell == 0:
                    node = Node(x, y)
                    self.nodes.append(node)
                    nodes_indexes[x][y] = i
                    self.indexesNodes[i] = node
                    i += 1
                x += 1
            y += 1

        nodes_count = len(self.nodes)
        distance_table = [[float('inf') for x in range(nodes_count)] for y in range(nodes_count)]
        next_nodes_table = [[None for x in range(nodes_count)] for y in range(nodes_count)]

        # initiate same nodes with zeros
        for x in range(nodes_count):
            distance_table[x][x] = 0

        # now put neighbours with their value = 1
        y = 0
        for row in self.board:
            x = 0
            for cell in row:
                if cell == 0:
                    xy_node_index = nodes_indexes[x][y]
                    if x > 0 and self.board[y][x - 1] == 0:
                        distance_table[xy_node_index][nodes_indexes[x - 1][y]] = 1
                        next_nodes_table[xy_node_index][nodes_indexes[x - 1][y]] = nodes_indexes[x - 1][y]
                    if x < max_x - 1 and self.board[y][x + 1] == 0:
                        distance_table[xy_node_index][nodes_indexes[x + 1][y]] = 1
                        next_nodes_table[xy_node_index][nodes_indexes[x + 1][y]] = nodes_indexes[x + 1][y]
                    if y > 0 and self.board[y - 1][x] == 0:
                        distance_table[xy_node_index][nodes_indexes[x][y - 1]] = 1
                        next_nodes_table[xy_node_index][nodes_indexes[x][y - 1]] = nodes_indexes[x][y - 1]
                    if y < max_y - 1 and self.board[y + 1][x] == 0:
                        distance_table[xy_node_index][nodes_indexes[x][y + 1]] = 1
                        next_nodes_table[xy_node_index][nodes_indexes[x][y + 1]] = nodes_indexes[x][y + 1]
                x += 1
            y += 1
        for u in self.nodes:
            for v1 in self.nodes:
                for v2 in self.nodes:
                    if v1.x == v2.x:
                        if v1.y == v2.y - 1 or v1.y == v2.y + 1 or v2.y == v1.y - 1 or v2.y == v1.y + 1:
                            continue
                    if v1.y == v2.y:
                        if v1.x == v2.x - 1 or v1.x == v2.x + 1 or v2.x == v1.x - 1 or v2.x == v1.x + 1:
                            continue
                    index_v1 = nodes_indexes[v1.x][v1.y]
                    index_v2 = nodes_indexes[v2.x][v2.y]
                    index_u = nodes_indexes[u.x][u.y]
                    possible_shorter_distance = distance_table[index_v1][index_u] + distance_table[index_u][index_v2]
                    if distance_table[index_v1][index_v2] > possible_shorter_distance:
                        distance_table[index_v1][index_v2] = possible_shorter_distance
                        next_nodes_table[index_v1][index_v2] = next_nodes_table[index_v1][index_u]

        # that are the only things that matters for us after all.
        self.nodesIndexes = nodes_indexes
        self.nextNodes = next_nodes_table

    def getnextmove(self, startnode, destnode):
        try:
            return self.indexesNodes[
                self.nextNodes[self.nodesIndexes[startnode.x][startnode.y]][self.nodesIndexes[destnode.x][destnode.y]]]
        except:
            return Node(0, 0)
