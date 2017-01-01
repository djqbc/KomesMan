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
        self.tripDistance = random.choice(list(range(2,11,2)))
        self.direction = _direction
        self.x = _x
        self.y = _y
        self.finished = False
        self.visited = [(_x, _y)]
        self.board[_x][_y] = BoardElement.EMPTY
    def drill(self):
        nextX = self.x
        nextY = self.y
        if self.direction == DrillDirection.UP:
            nextY -= 1
        if self.direction == DrillDirection.DOWN:
            nextY += 1
        if self.direction == DrillDirection.LEFT:
            nextX -= 1
        if self.direction == DrillDirection.RIGHT:
            nextX += 1
        if self.isBorder(nextX, nextY):
            self.tripDistance = random.choice(list(range(2,11,2)))
            self.changeDirection()
        elif self.board[nextX][nextY] == BoardElement.EMPTY and not (nextX, nextY) in self.visited:
            self.finished = True
        else:
            self.board[nextX][nextY] = BoardElement.EMPTY
            self.tripDistance -= 1
            self.x = nextX
            self.y = nextY
            self.visited += [(nextX, nextY)]
            if self.tripDistance == 0:
                self.tripDistance = random.choice(list(range(2,11,2)))
                self.changeDirection()
    def changeDirection(self):
        if self.direction == DrillDirection.UP:
            self.direction = random.choice([DrillDirection.LEFT, DrillDirection.RIGHT])
        elif self.direction == DrillDirection.DOWN:
            self.direction = random.choice([DrillDirection.LEFT, DrillDirection.RIGHT])
        elif self.direction == DrillDirection.LEFT:
            self.direction = random.choice([DrillDirection.UP, DrillDirection.DOWN])
        elif self.direction == DrillDirection.RIGHT:
            self.direction = random.choice([DrillDirection.UP, DrillDirection.DOWN])
    def isFinished(self):
        return self.finished
    def isBorder(self, _x=None, _y=None):
        if _x != None:
            return (_x == 0 or _y == 0 or _x == len(self.board) - 1 or _y == len(self.board[0]) - 1)
        else:
            return (self.x == 0 or self.y == 0 or self.x == len(self.board) - 1 or self.y == len(self.board[0]) - 1)
    def isCrossingBorder(self):
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
    def __init__(self, _board, _numberOfBuilders):
        self.board = _board
        self.drills = []
        usedRows = []
        usedColumns = []
        for _ in range(_numberOfBuilders):
            x = random.randint(1, len(self.board) - 2)
            y = random.randint(1, len(self.board[0]) - 2)
            while x in usedColumns or y in usedRows:
                x = random.randint(1, len(self.board) - 2)
                y = random.randint(1, len(self.board[0]) - 2)
            usedColumns += [x]
            usedRows += [y]
            tmp = [2] * 50 + [3] * 30 + [4] * 20
            numberOfDrills = random.choice(tmp)
            drillDirections = [DrillDirection.UP, DrillDirection.DOWN, DrillDirection.LEFT, DrillDirection.RIGHT]
            for _ in range(numberOfDrills):
                directionChances = []
                for d in drillDirections:
                    directionChances = directionChances + [d] * int(100 / len(drillDirections)) 
                direction = random.choice(directionChances)
                drillDirections.remove(direction)
                self.drills.append(Drill(self.board, direction, x, y))
    def drill(self):
        workToDo = True
        while workToDo:
            workToDo = False
            for drill in self.drills:
                if not drill.isFinished():
                    workToDo = True
                    drill.drill()

class GeneratedBoard:
    '''Class holding randomly generated board'''

    def get_board_binary(self, _sX=16, _sY=12):
        '''returns representation of randomly generated board'''

        board = [[BoardElement.WALL for _ in range(_sX)] for _ in range(_sY)] 
        allCells = _sY * _sX
        builder = Builder(board, 2)
        builder.drill()
        emptyCells = []
        for x in range(_sY):
            for y in range(_sX):
                if board[x][y] == BoardElement.EMPTY:
                    emptyCells += [(x, y)]
        emptyCellsLen = len(emptyCells)
        capsNumber = random.randint(int(emptyCellsLen / 10), int(emptyCellsLen / 2))
        for _ in range(capsNumber):
            cell = random.choice(emptyCells)
            emptyCells.remove(cell)
            board[cell[0]][cell[1]] = BoardElement.CAP
        
        #"wartosc mapy" - im wieksza tym wiecej ciekawych rzeczy ale tez wiecej wrogow
        LOWER_BOUND_CONSTANT = 10
        UPPER_BOUND_CONSTANT = 100
        BOARD_VALUE = random.randint(LOWER_BOUND_CONSTANT * emptyCellsLen, UPPER_BOUND_CONSTANT * emptyCellsLen)
        currentBoardValue = BOARD_VALUE
        print("BOARD_VALUE: ", BOARD_VALUE)
        prices = {
            BoardElement.BEER : 100,
            BoardElement.DRUG : 200,
            BoardElement.PILL : 500
            }
        while currentBoardValue > 0:
            availableItems = {item : price for item, price in prices.items() if price <= currentBoardValue}
            if len(availableItems) == 0:
                currentBoardValue = 0
            else:
                item = random.choice(list(availableItems))
                itemPrice = availableItems[item]
                x, y = random.choice(emptyCells)
                emptyCells.remove((x, y))
                board[x][y] = item
                currentBoardValue -= itemPrice
                
        #add komesman
        komesmanX, komesmanY = random.choice(emptyCells)
        emptyCells.remove((komesmanX, komesmanY))
        board[komesmanX][komesmanY] = BoardElement.KOMESMAN
        
        #add enemies
        currentBoardValue = BOARD_VALUE
        prices = {#dodac rozroznionych przeciwnikow
            BoardElement.ENEMY : 1000
            }
        while currentBoardValue > 0:
            availableEnemies = {item : price for item, price in prices.items() if price <= currentBoardValue}
            if len(availableEnemies) == 0:
                currentBoardValue = 0
            else:
                item = random.choice(list(availableEnemies.keys()))
                itemPrice = availableEnemies[item]
                dist = 0
                while dist <= 3:
                    x, y = random.choice(emptyCells)
                    dist = math.hypot(x - komesmanX, y - komesmanY)
                emptyCells.remove((x, y))
                board[x][y] = item
                currentBoardValue -= itemPrice
        
        return board