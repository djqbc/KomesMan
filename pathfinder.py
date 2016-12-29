from math import inf

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

class Pathfinder:

    def __init__(self, board):
        self.board = board
        self.nodes = []
        self.shortestPaths = {}

    def prepareAllStepsForShortestPaths(self):
        #Generate all edges of graph
        maxY = len(self.board)
        maxX = len(self.board[1])

        y = 0
        for row in self.board:
            x = 0
            for cell in row:
                if cell == 0:
                    self.nodes.append(Node(x,y))
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
                    if x>0 and self.board[y][x-1] == 0:
                        distanceTable[self.nodes.index(Node(x, y))][self.nodes.index(Node(x-1, y))] = 1
                        previousNodesTable[self.nodes.index(Node(x, y))][self.nodes.index(Node(x-1, y))] = self.nodes.index(Node(x, y))
                    if x<maxX-1 and self.board[y][x+1] == 0:
                        distanceTable[self.nodes.index(Node(x, y))][self.nodes.index(Node(x+1, y))] = 1
                        previousNodesTable[self.nodes.index(Node(x, y))][self.nodes.index(Node(x+1, y))] = self.nodes.index(Node(x, y))
                    if y>0 and self.board[y-1][x] == 0:
                        distanceTable[self.nodes.index(Node(x, y))][self.nodes.index(Node(x, y-1))] = 1
                        previousNodesTable[self.nodes.index(Node(x, y))][self.nodes.index(Node(x, y-1))] = self.nodes.index(Node(x, y))
                    if y<maxY-1 and self.board[y+1][x] == 0:
                        distanceTable[self.nodes.index(Node(x, y))][self.nodes.index(Node(x, y+1))] = 1
                        previousNodesTable[self.nodes.index(Node(x, y))][self.nodes.index(Node(x, y+1))] = self.nodes.index(Node(x, y))
                x+=1
            y+=1

            '''
            todo !!!
            dla każdego wierzchołka u  w V[G] wykonaj
                dla każdego wierzchołka v1 w V[G] wykonaj
                    dla każdego wierzchołka v2 w V[G] wykonaj
                    jeżeli
                    d[v1][v2] > d[v1][u] + d[u][v2] to
                        d[v1][v2] = d[v1][u] + d[u][v2]
                        poprzednik[v1][v2] = poprzednik[u][v2]
            '''

    def getNextMove(self, startx, starty, destx, desty):
        # todo ^^^ calkowite przerobienie na powyzsze...
        return self.shortestPaths[Edge(startx,starty,destx,desty)]
