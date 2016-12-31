from math import inf

from artifact.tagartifact import TagArtifact
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
        self.addArtifact(TagArtifact("PathFinder"))

    def prepareAllStepsForShortestPaths(self):
        #Generate all edges of graph
        maxY = len(self.board)
        maxX = len(self.board[1])
        nodesIndexes = {}
        self.indexesNodes = {}

        i=0
        y = 0
        for row in self.board:
            x = 0
            for cell in row:
                if cell == 0:
                    node = Node(x,y)
                    self.nodes.append(node)
                    nodesIndexes[node] = i
                    self.indexesNodes[i] = node
                    i+=1
                x+=1
            y+=1

        nodesCount = len(self.nodes)
        distanceTable = [ [inf for x in range(nodesCount)] for y in range(nodesCount)]
        previousNodesTable = [ [None for x in range(nodesCount)] for y in range(nodesCount)]

        #initiate same nodes with zeros
        for x in range(nodesCount):
            distanceTable[x][x] = 0

        # now put neighbours with their value = 1
        y = 0
        for row in self.board:
            x = 0
            for cell in row:
                if cell == 0:
                    xyNodeIndex = nodesIndexes[Node(x, y)]
                    if x>0 and self.board[y][x-1] == 0:
                        distanceTable[xyNodeIndex][nodesIndexes[Node(x-1, y)]] = 1
                        previousNodesTable[xyNodeIndex][nodesIndexes[Node(x-1, y)]] = xyNodeIndex
                    if x<maxX-1 and self.board[y][x+1] == 0:
                        distanceTable[xyNodeIndex][nodesIndexes[Node(x+1, y)]] = 1
                        previousNodesTable[xyNodeIndex][nodesIndexes[Node(x+1, y)]] = xyNodeIndex
                    if y>0 and self.board[y-1][x] == 0:
                        distanceTable[xyNodeIndex][nodesIndexes[Node(x, y-1)]] = 1
                        previousNodesTable[xyNodeIndex][nodesIndexes[Node(x, y-1)]] = xyNodeIndex
                    if y<maxY-1 and self.board[y+1][x] == 0:
                        distanceTable[xyNodeIndex][nodesIndexes[Node(x, y+1)]] = 1
                        previousNodesTable[xyNodeIndex][nodesIndexes[Node(x, y+1)]] = xyNodeIndex
                x+=1
            y+=1

        i = 0
        totaltodo = len(self.nodes)**3
        for u in self.nodes:
            for v1 in self.nodes:
                for v2 in self.nodes:
                    possible_shorter_distance = distanceTable[nodesIndexes[v1]][nodesIndexes[u]] = distanceTable[nodesIndexes[u]][nodesIndexes[v2]]
                    print(i/totaltodo, 'done...')
                    i+=1
                    if distanceTable[nodesIndexes[v1]][nodesIndexes[v2]] > possible_shorter_distance:
                        distanceTable[nodesIndexes[v1]][nodesIndexes[v2]] = possible_shorter_distance
                        previousNodesTable[nodesIndexes[v1]][nodesIndexes[v2]] = previousNodesTable[nodesIndexes[u]][nodesIndexes[v2]]

        #that are the onnly things that matters for us after all.
        self.nodesIndexes = nodesIndexes
        self.previousNodes = previousNodesTable

    def getNextMove(self, startnode, destnode):
        #TODO: Cos tu jest nie tak.
        # sprobuje juro przerobic algorytm
        # zeby sciezke zapisywal w 2 strone. Gdzies musialem sie walnąć.
        print('Getting path from: [{copX}, {copY}] to [{komX}, {komY}].'.format(copX=startnode.x, copY = startnode.y, komX = destnode.x, komY = destnode.y))
        node = self.indexesNodes[self.previousNodes[self.nodesIndexes[destnode]][self.nodesIndexes[startnode]]]
        print(node.x, node.y)
        while node.x != startnode.x and node.y != startnode.y:
            node = self.indexesNodes[self.previousNodes[self.nodesIndexes[destnode]][self.nodesIndexes[node]]]
            print(node.x, node.y)
        print('end')
        return self.indexesNodes[self.previousNodes[self.nodesIndexes[destnode]][self.nodesIndexes[startnode]]]
