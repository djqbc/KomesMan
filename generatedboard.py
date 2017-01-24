import random
from enum import Enum
from board import BoardElement
import math


class DrillDirection(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Drill:
    def __init__(self, _board, _direction, _x, _y):
        self.board = _board
        self.tripDistance = random.choice(list(range(2, 11, 2)))
        self.direction = _direction
        self.x = _x
        self.y = _y
        self.finished = False
        self.visited = [(_x, _y)]
        self.board[_x][_y] = BoardElement.EMPTY

    def drill(self):
        next_x = self.x
        next_y = self.y
        if self.direction == DrillDirection.UP:
            next_y -= 1
        if self.direction == DrillDirection.DOWN:
            next_y += 1
        if self.direction == DrillDirection.LEFT:
            next_x -= 1
        if self.direction == DrillDirection.RIGHT:
            next_x += 1
        if self.isborder(next_x, next_y):
            self.tripDistance = random.choice(list(range(2, 11, 2)))
            self.changedirection()
        elif self.board[next_x][next_y] == BoardElement.EMPTY and not (next_x, next_y) in self.visited:
            self.finished = True
        else:
            self.board[next_x][next_y] = BoardElement.EMPTY
            self.tripDistance -= 1
            self.x = next_x
            self.y = next_y
            self.visited += [(next_x, next_y)]
            if self.tripDistance == 0:
                self.tripDistance = random.choice(list(range(2, 11, 2)))
                self.changedirection()

    def changedirection(self):
        if self.direction == DrillDirection.UP:
            self.direction = random.choice([DrillDirection.LEFT, DrillDirection.RIGHT])
        elif self.direction == DrillDirection.DOWN:
            self.direction = random.choice([DrillDirection.LEFT, DrillDirection.RIGHT])
        elif self.direction == DrillDirection.LEFT:
            self.direction = random.choice([DrillDirection.UP, DrillDirection.DOWN])
        elif self.direction == DrillDirection.RIGHT:
            self.direction = random.choice([DrillDirection.UP, DrillDirection.DOWN])

    def isfinished(self):
        return self.finished

    def isborder(self, _x=None, _y=None):
        if _x is not None:
            return _x == 0 or _y == 0 or _x == len(self.board) - 1 or _y == len(self.board[0]) - 1
        else:
            return self.x == 0 or self.y == 0 or self.x == len(self.board) - 1 or self.y == len(self.board[0]) - 1

    def iscrossingborder(self):
        if self.direction == DrillDirection.UP and self.y == 0:
            return True
        if self.direction == DrillDirection.DOWN and self.y == len(self.board[0]) - 1:
            return True
        if self.direction == DrillDirection.LEFT and self.x == 0:
            return True
        if self.direction == DrillDirection.RIGHT and self.x == len(self.board) - 1:
            return True
        return False


class Builder:
    def __init__(self, _board, _numberofbuilders):
        self.board = _board
        self.drills = []
        used_rows = []
        used_columns = []
        for _ in range(_numberofbuilders):
            x = random.randint(1, len(self.board) - 2)
            y = random.randint(1, len(self.board[0]) - 2)
            while x in used_columns or y in used_rows:
                x = random.randint(1, len(self.board) - 2)
                y = random.randint(1, len(self.board[0]) - 2)
            used_columns += [x]
            used_rows += [y]
            tmp = [2] * 50 + [3] * 30 + [4] * 20
            number_of_drills = random.choice(tmp)
            drill_directions = [DrillDirection.UP, DrillDirection.DOWN, DrillDirection.LEFT, DrillDirection.RIGHT]
            for _ in range(number_of_drills):
                direction_chances = []
                for d in drill_directions:
                    direction_chances = direction_chances + [d] * int(100 / len(drill_directions))
                direction = random.choice(direction_chances)
                drill_directions.remove(direction)
                self.drills.append(Drill(self.board, direction, x, y))

    def drill(self):
        work_to_do = True
        while work_to_do:
            work_to_do = False
            for drill in self.drills:
                if not drill.isfinished():
                    work_to_do = True
                    drill.drill()


class GeneratedBoard:
    """Class holding randomly generated board"""

    @staticmethod
    def get_board_binary(_sx, _sy):
        """returns representation of randomly generated board"""

        board = [[BoardElement.WALL for _ in range(_sx)] for _ in range(_sy)]
        builder = Builder(board, 4)
        builder.drill()
        empty_cells = []
        for x in range(_sy):
            for y in range(_sx):
                if board[x][y] == BoardElement.EMPTY:
                    empty_cells += [(x, y)]
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
                x, y = random.choice(empty_cells)
                empty_cells.remove((x, y))
                board[x][y] = item
                current_board_value -= item_price

        # add komesman
        komesman_x, komesman_y = random.choice(empty_cells)
        empty_cells.remove((komesman_x, komesman_y))
        board[komesman_x][komesman_y] = BoardElement.KOMESMAN

        # add enemies
        current_board_value = board_value
        prices = {  # dodac rozroznionych przeciwnikow
            BoardElement.ENEMY: board_value
        }
        while current_board_value > 0:
            available_enemies = {item: price for item, price in prices.items() if price <= current_board_value}
            if len(available_enemies) == 0:
                current_board_value = 0
            else:
                item = random.choice(list(available_enemies.keys()))
                item_price = available_enemies[item]
                dist = 0
                while dist <= 3:
                    x, y = random.choice(empty_cells)
                    dist = math.hypot(x - komesman_x, y - komesman_y)
                empty_cells.remove((x, y))
                board[x][y] = item
                current_board_value -= item_price

        return board
