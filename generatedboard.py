"""
Generated board module
"""

import random
from enum import Enum
import math
from board import BoardElement


class DrillDirection(Enum):
    """
    Enum representing direction of drill.
    """
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Drill:
    """
    Drill class
    """
    def __init__(self, _board, _direction, _x, _y):
        """
        Constructor
        :param _board: Board to be drilled (2d array of BoardElement values)
        :param _direction: Initial direction of drill
        :param _x: Start X tile position of drill
        :param _y: Start Y tile position of drill
        """
        self.board = _board
        self.trip_distance = random.choice(list(range(2, 11, 2)))
        self.direction = _direction
        self.node_x = _x
        self.node_y = _y
        self.finished = False
        self.visited = [(_x, _y)]
        self.board[_x][_y] = BoardElement.EMPTY

    def drill(self):
        """
        Perform drilling of board.
        :return: nothing
        """
        next_x = self.node_x
        next_y = self.node_y
        if self.direction == DrillDirection.UP:
            next_y -= 1
        if self.direction == DrillDirection.DOWN:
            next_y += 1
        if self.direction == DrillDirection.LEFT:
            next_x -= 1
        if self.direction == DrillDirection.RIGHT:
            next_x += 1
        if self.isborder(next_x, next_y):
            self.trip_distance = random.choice(list(range(2, 11, 2)))
            self.changedirection()
        elif self.board[next_x][next_y] == BoardElement.EMPTY and not (next_x, next_y) in self.visited:
            self.finished = True
        else:
            self.board[next_x][next_y] = BoardElement.EMPTY
            self.trip_distance -= 1
            self.node_x = next_x
            self.node_y = next_y
            self.visited += [(next_x, next_y)]
            if self.trip_distance == 0:
                self.trip_distance = random.choice(list(range(2, 11, 2)))
                self.changedirection()

    def changedirection(self):
        """
        Randomly changes direction of drill based on previous direction
        :return: nothing
        """
        if self.direction == DrillDirection.UP:
            self.direction = random.choice([DrillDirection.LEFT, DrillDirection.RIGHT])
        elif self.direction == DrillDirection.DOWN:
            self.direction = random.choice([DrillDirection.LEFT, DrillDirection.RIGHT])
        elif self.direction == DrillDirection.LEFT:
            self.direction = random.choice([DrillDirection.UP, DrillDirection.DOWN])
        elif self.direction == DrillDirection.RIGHT:
            self.direction = random.choice([DrillDirection.UP, DrillDirection.DOWN])

    def isfinished(self):
        """
        Return if drill finished work
        :return: True if drill finished, False otherwise.
        """
        return self.finished

    def isborder(self, nodex=None, nodey=None):
        """
        Checks if X,Y (tile positions) are borders of board.
        :param nodex: X number of tile, or None if this parameter should be taken from Drill.
        :param nodey: Y number of tile, or None if this parameter should be taken from Drill.
        :return: True if tile is on border, False otherwise.
        """
        if nodex is not None:
            return nodex == 0 or nodey == 0 or nodex == len(self.board) - 1 or nodey == len(self.board[0]) - 1
        else:
            return self.node_x == 0 or self.node_y == 0 or self.node_x == len(self.board) - 1 or self.node_y == len(self.board[0]) - 1

    def iscrossingborder(self):
        """
        Check if drill is going outside board
        :return: True if drill is goingo outside board, False otherwise.
        """
        if self.direction == DrillDirection.UP and self.node_y == 0:
            return True
        if self.direction == DrillDirection.DOWN and self.node_y == len(self.board[0]) - 1:
            return True
        if self.direction == DrillDirection.LEFT and self.node_x == 0:
            return True
        if self.direction == DrillDirection.RIGHT and self.node_x == len(self.board) - 1:
            return True
        return False


class Builder:
    """
    Builder class
    """
    def __init__(self, _board, _numberofbuilders):
        """
        Constructor
        :param _board: Board which should be drilled (probably full of BoardElement.Wall)
        :param _numberofbuilders: Number of drills for creating board.
        """
        self.board = _board
        self.drills = []
        used_rows = []
        used_columns = []
        for _ in range(_numberofbuilders):
            tmp_x = random.randint(1, len(self.board) - 2)
            tmp_y = random.randint(1, len(self.board[0]) - 2)
            while tmp_x in used_columns or tmp_y in used_rows:
                tmp_x = random.randint(1, len(self.board) - 2)
                tmp_y = random.randint(1, len(self.board[0]) - 2)
            used_columns += [tmp_x]
            used_rows += [tmp_y]
            tmp = [2] * 50 + [3] * 30 + [4] * 20
            number_of_drills = random.choice(tmp)
            drill_directions = [DrillDirection.UP, DrillDirection.DOWN, DrillDirection.LEFT, DrillDirection.RIGHT]
            for _ in range(number_of_drills):
                direction_chances = []
                for drill_d in drill_directions:
                    direction_chances = direction_chances + [drill_d] * int(100 / len(drill_directions))
                direction = random.choice(direction_chances)
                drill_directions.remove(direction)
                self.drills.append(Drill(self.board, direction, tmp_x, tmp_y))

    def drill(self):
        """
        Runs drilling on all drills until drilling is finished.
        :return: nothing
        """
        work_to_do = True
        while work_to_do:
            work_to_do = False
            for drill in self.drills:
                if not drill.isfinished():
                    work_to_do = True
                    drill.drill()

    def getneighbours(self, node_v):
        """
        Get not-yet drilled neighbours of certain coordinate.
        :param node_v: tuple of coordinates
        :return:
        """
        max_y = len(self.board[0])
        max_x = len(self.board)
        tmp_x, tmp_y = node_v
        result = []
        if tmp_x > 0 and self.board[tmp_x - 1][tmp_y] != BoardElement.WALL:
            result.append((tmp_x - 1, tmp_y))
        if tmp_y > 0 and self.board[tmp_x][tmp_y - 1] != BoardElement.WALL:
            result.append((tmp_x, tmp_y - 1))
        if tmp_x + 1 < max_x and self.board[tmp_x + 1][tmp_y] != BoardElement.WALL:
            result.append((tmp_x + 1, tmp_y))
        if tmp_y + 1 < max_y and self.board[tmp_x][tmp_y + 1] != BoardElement.WALL:
            result.append((tmp_x, tmp_y + 1))
        return result

    def isconnected(self):
        """
        Is graph connected?
        :return: True if graph is connected, False otherwise.
        """
        max_y = len(self.board[0])
        max_x = len(self.board)
        graph = []
        for tmp_x in range(max_x):
            for tmp_y in range(max_y):
                if self.board[tmp_x][tmp_y] != BoardElement.WALL:
                    graph += [(tmp_x, tmp_y)]
        graph_len = len(graph)
        visited = [False for _ in range(graph_len)]
        stack = []
        visited_count = 0
        stack.append(graph[0])
        visited[0] = True
        while len(stack) > 0:
            tmp_v = stack.pop()
            visited_count += 1
            for tmp_u in self.getneighbours(tmp_v):
                i = graph.index(tmp_u)
                if not visited[i]:
                    visited[i] = True
                    stack.append(tmp_u)
        return visited_count == graph_len

class GeneratedBoard:
    """
    Class holding randomly generated board
    """

    @staticmethod
    def get_board_binary(_sx, _sy):
        """
        Returns representation of randomly generated board
        :param _sx: number of tiles in X dimension
        :param _sy: number of tiles in Y dimension
        :return: Board in enum format (with simple walls and items)
        """

        board = [[BoardElement.WALL for _ in range(_sx)] for _ in range(_sy)]
        builder = Builder(board, 4)
        builder.drill()
        while not builder.isconnected():
            print("Unconnected graph - generating again....")
            board = [[BoardElement.WALL for _ in range(_sx)] for _ in range(_sy)]
            builder = Builder(board, 4)
            builder.drill()

        empty_cells = []
        for tmp_x in range(_sy):
            for tmp_y in range(_sx):
                if board[tmp_x][tmp_y] == BoardElement.EMPTY:
                    empty_cells += [(tmp_x, tmp_y)]
        empty_cells_len = len(empty_cells)
        caps_number = random.randint(int(empty_cells_len / 10), int(empty_cells_len / 2))
        for _ in range(caps_number):
            cell = random.choice(empty_cells)
            empty_cells.remove(cell)
            board[cell[0]][cell[1]] = BoardElement.CAP

        # "wartosc mapy" - im wieksza tym wiecej ciekawych rzeczy ale tez wiecej wrogow
        lower_bound_constant = 10
        upper_bound_constant = 100
        board_value = random.randint(lower_bound_constant * empty_cells_len, upper_bound_constant * empty_cells_len)
        current_board_value = board_value
        print("BOARD_VALUE: ", board_value)
        prices = {
            BoardElement.BEER: 200,
            BoardElement.DRUG: 400,
            BoardElement.PILL: 1000
        }
        while current_board_value > 0:
            available_items = {item: price for item, price in prices.items() if price <= current_board_value}
            if len(available_items) == 0:
                current_board_value = 0
            else:
                item = random.choice(list(available_items))
                item_price = available_items[item]
                tmp_x, tmp_y = random.choice(empty_cells)
                empty_cells.remove((tmp_x, tmp_y))
                board[tmp_x][tmp_y] = item
                current_board_value -= item_price

        # add komesman
        komesman_x, komesman_y = random.choice(empty_cells)
        empty_cells.remove((komesman_x, komesman_y))
        board[komesman_x][komesman_y] = BoardElement.KOMESMAN

        # add enemies
        current_board_value = board_value
        prices = {  # dodac rozroznionych przeciwnikow
            BoardElement.ENEMY: 1500
        }

        i = 0
        while current_board_value > 0 and i<3:
            available_enemies = {item: price for item, price in prices.items() if price <= current_board_value}
            if len(available_enemies) == 0:
                current_board_value = 0
            else:
                item = random.choice(list(available_enemies.keys()))
                item_price = available_enemies[item]
                dist = 0
                while dist <= 3:
                    tmp_x, tmp_y = random.choice(empty_cells)
                    dist = math.hypot(tmp_x - komesman_x, tmp_y - komesman_y)
                empty_cells.remove((tmp_x, tmp_y))
                board[tmp_x][tmp_y] = item
                current_board_value -= item_price
                i+= 1

        return board
