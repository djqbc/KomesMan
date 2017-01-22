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
        self.addArtifact(TagArtifact(TagType.OTHER, TagSubType.PATHFINDER))

    def prepareAllStepsForShortestPaths(self):
        # Generate all edges of graph
        maxY = len(self.board)
        maxX = len(self.board[1])
        nodesIndexes = [[0 for x in range(maxY)] for y in range(maxX)]
        self.indexesNodes.clear()

        i = 0
        y = 0
        for row in self.board:
            x = 0
            for cell in row:
                if cell == 0:
                    node = Node(x, y)
                    self.nodes.append(node)
                    nodesIndexes[x][y] = i
                    self.indexesNodes[i] = node
                    i += 1
                x += 1
            y += 1

        nodesCount = len(self.nodes)
        distanceTable = [[float('inf') for x in range(nodesCount)] for y in range(nodesCount)]
        nextNodesTable = [[None for x in range(nodesCount)] for y in range(nodesCount)]

        # initiate same nodes with zeros
        for x in range(nodesCount):
            distanceTable[x][x] = 0

        # now put neighbours with their value = 1
        y = 0
        for row in self.board:
            x = 0
            for cell in row:
                if cell == 0:
                    xyNodeIndex = nodesIndexes[x][y]
                    if x > 0 and self.board[y][x - 1] == 0:
                        distanceTable[xyNodeIndex][nodesIndexes[x - 1][y]] = 1
                        nextNodesTable[xyNodeIndex][nodesIndexes[x - 1][y]] = nodesIndexes[x - 1][y]
                    if x < maxX - 1 and self.board[y][x + 1] == 0:
                        distanceTable[xyNodeIndex][nodesIndexes[x + 1][y]] = 1
                        nextNodesTable[xyNodeIndex][nodesIndexes[x + 1][y]] = nodesIndexes[x + 1][y]
                    if y > 0 and self.board[y - 1][x] == 0:
                        distanceTable[xyNodeIndex][nodesIndexes[x][y - 1]] = 1
                        nextNodesTable[xyNodeIndex][nodesIndexes[x][y - 1]] = nodesIndexes[x][y - 1]
                    if y < maxY - 1 and self.board[y + 1][x] == 0:
                        distanceTable[xyNodeIndex][nodesIndexes[x][y + 1]] = 1
                        nextNodesTable[xyNodeIndex][nodesIndexes[x][y + 1]] = nodesIndexes[x][y + 1]
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
                    indexV1 = nodesIndexes[v1.x][v1.y]
                    indexV2 = nodesIndexes[v2.x][v2.y]
                    indexU = nodesIndexes[u.x][u.y]
                    possible_shorter_distance = distanceTable[indexV1][indexU] + distanceTable[indexU][indexV2]
                    if distanceTable[indexV1][indexV2] > possible_shorter_distance:
                        distanceTable[indexV1][indexV2] = possible_shorter_distance
                        nextNodesTable[indexV1][indexV2] = nextNodesTable[indexV1][indexU]

        # that are the only things that matters for us after all.
        self.nodesIndexes = nodesIndexes
        self.nextNodes = nextNodesTable

    def getNextMove(self, startnode, destnode):
        try:
            return self.indexesNodes[
                self.nextNodes[self.nodesIndexes[startnode.x][startnode.y]][self.nodesIndexes[destnode.x][destnode.y]]]
        except:
            return Node(0, 0)
