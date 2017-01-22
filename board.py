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
    def __init__(self, board, systems, registerlist, tilesize=64):
        super(Board, self).__init__()
        self.map = [[Entity() for x in range(len(board))] for y in range(len(board[0]))]
        self.boardData = board
        self.tileSize = tilesize
        i_x = 0
        for row in board:
            i_y = 0
            for cell in row:
                if cell != 0:
                    tile_sprite = WallSprite(cell)
                    self.map[i_y][i_x].addartifact(
                        SpriteArtifact(tile_sprite, i_y * tilesize, i_x * tilesize, GameState.GAME))
                    systems[DrawSystem.NAME].register(self.map[i_y][i_x])
                    registerlist.append(self.map[i_y][i_x])
                i_y += 1
            i_x += 1
        self.addartifact(TagArtifact(TagType.FIXED, TagSubType.BOARD))
        systems[TagSystem.NAME].register(self)
        registerlist.append(self)

    def getpos(self, pos):
        return int(pos / self.tileSize)

    def checknext(self, pos):
        return pos % self.tileSize != 0

    def isbeyondborder(self, _x, _y):
        if _x < 0 or _y < 0 or _x > len(self.boardData[0]) * self.tileSize or _y > len(self.boardData) * self.tileSize:
            return True
        return False

    def checkmove(self, _posx, _posy, _dx, _dy):
        try:
            if self.isbeyondborder(_posx + _dx, _posy + _dy):
                return False
            if _dx < 0:  # left
                if self.boardData[self.getpos(_posy)][self.getpos(_posx - 1)] != 0 or (
                    (self.checknext(_posy)) and (self.boardData[self.getpos(_posy) + 1][self.getpos(_posx - 1)] != 0)):
                    return False

            if _dx > 0:  # right
                if self.boardData[self.getpos(_posy)][self.getpos(_posx) + 1] != 0 or (
                    (self.checknext(_posy)) and (self.boardData[self.getpos(_posy) + 1][self.getpos(_posx) + 1] != 0)):
                    return False

            if _dy < 0:  # up
                if self.boardData[self.getpos(_posy - 1)][self.getpos(_posx)] != 0 or (
                    (self.checknext(_posx)) and (self.boardData[self.getpos(_posy - 1)][self.getpos(_posx) + 1] != 0)):
                    return False

            if _dy > 0:  # down
                if self.boardData[self.getpos(_posy) + 1][self.getpos(_posx)] != 0 or (
                    (self.checknext(_posx)) and (self.boardData[self.getpos(_posy) + 1][self.getpos(_posx) + 1] != 0)):
                    return False
        except:
            return False
        return True
