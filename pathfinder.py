"""Pathfinder module."""

from threading import Thread
from artifact.tagartifact import TagArtifact, TagType, TagSubType
from entity import Entity


class Node:
    """Node class for pathfinder."""

    def __init__(self, x, y):
        """
        Constructor.

        :param node_x: X tile position of node.
        :param node_y: Y tile position of node.
        """
        self.node_x = x
        self.node_y = y

    def __hash__(self):
        """
        Return hash of Node.

        :return: hash of node
        """
        return hash((self.node_x, self.node_y))

    def __eq__(self, other):
        """
        Check for equality of Nodes.

        :param other: Second node to compare to
        :return: True if equal, false if not
        """
        return (self.node_x, self.node_y) == (other.node_x, other.node_y)

    def __ne__(self, other):
        """
        Check for not ewuality of Nodes.

        :param other: Second node to compare to
        :return: True if are not equal, False otherwise.
        """
        return not self == other


class Edge:
    """Edge between two nodes."""

    def __init__(self, u, v):
        """
        Constructor.

        :param node_u: 1st node
        :param node_v: 2nd node
        """
        self.node_u = u
        self.node_v = v

    def __hash__(self):
        """
        Return hash of Edge.

        :return: hash of Edge
        """
        return hash((self.node_u, self.node_v))

    def __eq__(self, other):
        """
        Check for equality of Edges.

        :param other: Second edge to compare to
        :return: True if equal, false if not
        """
        return (self.node_u, self.node_v) == (other.node_u, other.node_v)

    def __ne__(self, other):
        """
        Check for not ewuality of Edge.

        :param other: Second edge to compare to
        :return: True if are not equal, False otherwise.
        """
        return not self == other


class Pathfinder(Entity):
    """
    Class creating shortest paths between all nodes.

    Using Floyd-Warshall Alghorithm!
    """

    def __init__(self, board):
        """
        Constructor.

        :param board: binary representation of board for generation of shortest paths.
        """
        super(Pathfinder, self).__init__()
        self.board = board
        self.nodes = []
        #self.shortestPaths = {}
        self.indexes_nodes = {}
        self.nodes_indexes = []
        self.next_nodes = []
        self.addartifact(TagArtifact(TagType.OTHER, TagSubType.PATHFINDER))
        self.ready = False

    def prepareallstepsforshortestpaths(self):
        """
        Run preparation in seperate thread.

        :return: nothing
        """
        self.ready = False
        my_thread = Thread(target=self.workerthread, args=())
        my_thread.daemon = True
        my_thread.start()

    def workerthread(self):
        """
        Prepare all shortest paths.

        They are accessible via next_nodes.
        Each node has coressponding index in pathfinder, and nodes should be accessed self.NodesIndexes
        Node index can be converted back by use of self.indexes_nodes.
        Example usage:
        self.indexes_nodes[self.next_nodes[[self.nodes_indexes[self.nodes_indexes[sx][sy]][self.nodes_indexes[dx][dy]]]]]
        Where (sx, sy) - start point, (dx, dy) - destination

        :return: nothing
        """
        # Generate all edges of graph
        max_y = len(self.board)
        max_x = len(self.board[1])
        nodes_indexes = [[0 for tmp_x in range(max_y)] for tmp_y in range(max_x)]
        self.indexes_nodes.clear()

        i = 0
        tmp_y = 0
        for row in self.board:
            tmp_x = 0
            for cell in row:
                if cell == 0:
                    node = Node(tmp_x, tmp_y)
                    self.nodes.append(node)
                    nodes_indexes[tmp_x][tmp_y] = i
                    #self.indexes_nodes.append(node)
                    self.indexes_nodes[i] = node
                    i += 1
                tmp_x += 1
            tmp_y += 1

        nodes_count = len(self.nodes)
        distance_table = [[float('inf') for tmp_x in range(nodes_count)] for tmp_y in range(nodes_count)]
        next_nodes_table = [[None for tmp_x in range(nodes_count)] for tmp_y in range(nodes_count)]

        # initiate same nodes with zeros
        for tmp_x in range(nodes_count):
            distance_table[tmp_x][tmp_x] = 0

        # now put neighbours with their value = 1
        tmp_y = 0
        for row in self.board:
            tmp_x = 0
            for cell in row:
                if cell == 0:
                    xy_node_index = nodes_indexes[tmp_x][tmp_y]
                    if tmp_x > 0 and self.board[tmp_y][tmp_x - 1] == 0:
                        distance_table[xy_node_index][nodes_indexes[tmp_x - 1][tmp_y]] = 1
                        next_nodes_table[xy_node_index][nodes_indexes[tmp_x - 1][tmp_y]] = nodes_indexes[tmp_x - 1][tmp_y]
                    if tmp_x < max_x - 1 and self.board[tmp_y][tmp_x + 1] == 0:
                        distance_table[xy_node_index][nodes_indexes[tmp_x + 1][tmp_y]] = 1
                        next_nodes_table[xy_node_index][nodes_indexes[tmp_x + 1][tmp_y]] = nodes_indexes[tmp_x + 1][tmp_y]
                    if tmp_y > 0 and self.board[tmp_y - 1][tmp_x] == 0:
                        distance_table[xy_node_index][nodes_indexes[tmp_x][tmp_y - 1]] = 1
                        next_nodes_table[xy_node_index][nodes_indexes[tmp_x][tmp_y - 1]] = nodes_indexes[tmp_x][tmp_y - 1]
                    if tmp_y < max_y - 1 and self.board[tmp_y + 1][tmp_x] == 0:
                        distance_table[xy_node_index][nodes_indexes[tmp_x][tmp_y + 1]] = 1
                        next_nodes_table[xy_node_index][nodes_indexes[tmp_x][tmp_y + 1]] = nodes_indexes[tmp_x][tmp_y + 1]
                tmp_x += 1
            tmp_y += 1
        for tmp_u in self.nodes:
            for tmp_v1 in self.nodes:
                for tmp_v2 in self.nodes:
                    if tmp_v1.node_x == tmp_v2.node_x:
                        if tmp_v1.node_y == tmp_v2.node_y - 1 or tmp_v1.node_y == tmp_v2.node_y + 1 or tmp_v2.node_y == tmp_v1.node_y - 1 or tmp_v2.node_y == tmp_v1.node_y + 1:
                            continue
                    if tmp_v1.node_y == tmp_v2.node_y:
                        if tmp_v1.node_x == tmp_v2.node_x - 1 or tmp_v1.node_x == tmp_v2.node_x + 1 or tmp_v2.node_x == tmp_v1.node_x - 1 or tmp_v2.node_x == tmp_v1.node_x + 1:
                            continue
                    index_v1 = nodes_indexes[tmp_v1.node_x][tmp_v1.node_y]
                    index_v2 = nodes_indexes[tmp_v2.node_x][tmp_v2.node_y]
                    index_u = nodes_indexes[tmp_u.node_x][tmp_u.node_y]
                    possible_shorter_distance = distance_table[index_v1][index_u] + distance_table[index_u][index_v2]
                    if distance_table[index_v1][index_v2] > possible_shorter_distance:
                        distance_table[index_v1][index_v2] = possible_shorter_distance
                        next_nodes_table[index_v1][index_v2] = next_nodes_table[index_v1][index_u]

        # that are the only things that matters for us after all.
        self.nodes_indexes = nodes_indexes
        self.next_nodes = next_nodes_table
        print("Finish")
        self.ready = True

    def getnextmove(self, startnode, destnode):
        """
        Get next move.

        :param startnode: starting node
        :param destnode: destination node
        :return: new target node
        """
        try:
            if self.ready:
                return self.indexes_nodes[
                    self.next_nodes[self.nodes_indexes[startnode.node_x][startnode.node_y]][self.nodes_indexes[destnode.node_x][destnode.node_y]]]
            else:
                return destnode
        except:
            return Node(0, 0)
