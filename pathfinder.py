# from math import inf

from artifact.tagartifact import TagArtifact, TagType, TagSubType
from entity import Entity
from threading import Thread


class Node:
    """
    Node class for pathfinder.
    """
    def __init__(self, x, y):
        """
        Constructor
        :param x: X tile position of node.
        :param y: Y tile position of node.
        """
        self.x = x
        self.y = y

    def __hash__(self):
        """
        Returns hash of Node.
        :return: hash of node
        """
        return hash((self.x, self.y))

    def __eq__(self, other):
        """
        Check for equality of Nodes
        :param other: Second node to compare to
        :return: True if equal, false if not
        """
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        """
        Check for not ewuality of Nodes.
        :param other: Second node to compare to
        :return: True if are not equal, False otherwise.
        """
        return not (self == other)


class Edge:
    """
    Edge between two nodes.
    """
    def __init__(self, u, v):
        """
        Constructor
        :param u: 1st node
        :param v: 2nd node
        """
        self.u = u
        self.v = v

    def __hash__(self):
        """
        Returns hash of Edge
        :return: hash of Edge
        """
        return hash((self.u, self.v))

    def __eq__(self, other):
        """
        Check for equality of Edges
        :param other: Second edge to compare to
        :return: True if equal, false if not
        """
        return (self.u, self.v) == (other.u, other.v)

    def __ne__(self, other):
        """
        Check for not ewuality of Edge
        :param other: Second edge to compare to
        :return: True if are not equal, False otherwise.
        """
        return not (self == other)


class Pathfinder(Entity):
    """
    Class creating shortest paths between all nodes!
    Using Floyd-Warshall Alghorithm!
    """
    def __init__(self, board):
        """
        Constructor
        :param board: binary representation of board for generation of shortest paths.
        """
        super(Pathfinder, self).__init__()
        self.board = board
        self.nodes = []
        #self.shortestPaths = {}
        self.indexesNodes = {}
        self.nodesIndexes = []
        self.nextNodes = []
        self.addartifact(TagArtifact(TagType.OTHER, TagSubType.PATHFINDER))
        self.ready = False

    def prepareallstepsforshortestpaths(self):
        """
        Run preparation in seperate thread.
        :return: nothing
        """
        self.ready = False
        t = Thread(target=self.prepareallstepsforshortestpaths_, args=())
        t.daemon = True
        t.start()

    def prepareallstepsforshortestpaths_(self):
        """
        Prepares all shortest paths.
        They are accessible via nextNodes.
        Each node has coressponding index in pathfinder, and nodes should be accessed self.NodesIndexes
        Node index can be converted back by use of self.indexesNodes.
        Example usage:
        self.indexesNodes[self.nextNodes[[self.nodesIndexes[self.nodesIndexes[sx][sy]][self.nodesIndexes[dx][dy]]]]]
        Where (sx, sy) - start point, (dx, dy) - destination

        :return: nothing
        """
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
                    #self.indexesNodes.append(node)
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
        print("Finish")
        self.ready = True

    def getnextmove(self, startnode, destnode):
        try:
            if self.ready:
                return self.indexesNodes[
                    self.nextNodes[self.nodesIndexes[startnode.x][startnode.y]][self.nodesIndexes[destnode.x][destnode.y]]]
            else:
                return destnode
        except:
            return Node(0, 0)
