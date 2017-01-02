from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagArtifact, TagType, TagSubType
from entity import Entity
from sprite.wallsprite import WallSprite

from system.drawsystem import DrawSystem
from system.tagsystem import TagSystem
from system.gamesystem import GameState

from enum import IntEnum

class BoardElement(IntEnum):
    EMPTY = 0
    WALL = 1
    CAP = 2
    BEER = 3
    DRUG = 4
    PILL = 5
    ENEMY = 6
    KOMESMAN = 7
    TELEPORT = 8

class Board(Entity):
    def __init__(self, board, systems, registerList, tilesize=64):
        super(Board, self).__init__()
        self.map = [[Entity() for x in range(len(board))] for y in range(len(board[0]))]
        self.boardData = board
        self.tileSize = tilesize
        iX = 0
        for row in board:
            iY = 0
            for cell in row:
                if cell != 0:
                    tileSprite = WallSprite(cell)
                    self.map[iY][iX].addArtifact(SpriteArtifact(tileSprite, iY*tilesize, iX*tilesize, GameState.GAME))                    
                    systems[DrawSystem.NAME].register(self.map[iY][iX])
                    registerList.append(self.map[iY][iX])
                iY += 1
            iX += 1
        self.addArtifact(TagArtifact(TagType.FIXED, TagSubType.BOARD))
        systems[TagSystem.NAME].register(self)
        registerList.append(self)

    def getPos(self, pos):
        return int(pos/self.tileSize)

    def checkNext(self, pos):
        return pos % self.tileSize != 0
    
    def isBeyondBorder(self, _x, _y):
        if _x < 0 or _y < 0 or _x > len(self.boardData[0]) * self.tileSize or _y > len(self.boardData) * self.tileSize:
            return True
        return False
    def checkMove(self, _posX, _posY, _dX, _dY):
        try:
            if self.isBeyondBorder(_posX + _dX, _posY + _dY):
                return False
            if _dX < 0 : # left
                if self.boardData[self.getPos(_posY)][self.getPos(_posX-1)] != 0 or ( (self.checkNext(_posY)) and (self.boardData[self.getPos(_posY)+1][self.getPos(_posX-1)] != 0)):
                    return False
    
            if _dX > 0 : # right
                if self.boardData[self.getPos(_posY)][self.getPos(_posX)+1] != 0 or ( (self.checkNext(_posY)) and (self.boardData[self.getPos(_posY)+1][self.getPos(_posX)+1] != 0)):
                    return False
    
            if _dY < 0 : # up
                if self.boardData[self.getPos(_posY-1)][self.getPos(_posX)] != 0 or ( (self.checkNext(_posX)) and (self.boardData[self.getPos(_posY-1)][self.getPos(_posX)+1] != 0) ):
                    return False
    
            if _dY > 0 : # down
                if self.boardData[self.getPos(_posY)+1][self.getPos(_posX)] != 0 or ( (self.checkNext(_posX)) and (self.boardData[self.getPos(_posY)+1][self.getPos(_posX)+1] != 0) ):
                    return False
        except:
            return False
        return True