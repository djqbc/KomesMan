"""
Board module
"""
from enum import IntEnum
from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagArtifact, TagType, TagSubType
from entity import Entity
from sprite.wallsprite import WallSprite

from system.drawsystem import DrawSystem
from system.tagsystem import TagSystem
from system.gamesystem import GameState



class BoardElement(IntEnum):
    """
    Enum representing kinds of items which can be placed on board!
    """
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
    """
    Board class
    """
    def __init__(self, board, systems, registerlist, tilesize):
        """
        Constructor.
        :param board: Board - 2d array of WallKind items or 0's if there is no wall.
        :param systems: Collection of all systems
        :param registerlist: List where entities should be registered.
        :param tilesize: Tile size of board in pixels
        """
        super(Board, self).__init__()
        self.map = [[Entity() for _ in range(len(board))] for _ in range(len(board[0]))]
        self.board_data = board
        self.tile_size = tilesize
        i_x = 0
        for row in board:
            i_y = 0
            for cell in row:
                if cell != 0:
                    tile_sprite = WallSprite(cell, tilesize)
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
        """
        Returns "tile" position, from "pixel" position
        :param pos: position in pixels in specified dimension
        :return: integer tile position.
        """
        return int(pos / self.tile_size)

    def checknext(self, pos):
        """
        Defines if another tile should be checked for possibility of move
        :param pos: Pixel position in specified dimension
        :return: True if another tile should be checked, false otherwise.
        """
        return pos % self.tile_size != 0

    def isbeyondborder(self, pos_x, pos_y):
        """
        Check if specified pixel location is outside border
        :param pos_x: X integer position
        :param pos_y: Y integer position
        :return: true if pixel is beyond border, false otherwise.
        """
        if pos_x < 0 or pos_y < 0 or pos_x > len(self.board_data[0]) * self.tile_size or pos_y > len(self.board_data) * self.tile_size:
            return True
        return False

    def checkmove(self, pos_x, pos_y, delta_x, delta_y):
        """
        Check if specified move is possible
        :param pos_x: Current X (pixels) position of moved object
        :param pos_y: Current Y (pixels) position of moved object
        :param delta_x: Amount of X pixels to move (if <0 move lest, if >0 move right)
        :param delta_y: Amount of Y pixels to move (if <0 move up, if >0 move down)
        :return: true if move possible, false otherwise.
        """
        try:
            if self.isbeyondborder(pos_x + delta_x, pos_y + delta_y):
                return False
            if delta_x < 0:  # left
                if self.board_data[self.getpos(pos_y)][self.getpos(pos_x - 1)] != 0 or (
                    (self.checknext(pos_y)) and (self.board_data[self.getpos(pos_y) + 1][self.getpos(pos_x - 1)] != 0)):
                    return False

            if delta_x > 0:  # right
                if self.board_data[self.getpos(pos_y)][self.getpos(pos_x) + 1] != 0 or (
                    (self.checknext(pos_y)) and (self.board_data[self.getpos(pos_y) + 1][self.getpos(pos_x) + 1] != 0)):
                    return False

            if delta_y < 0:  # up
                if self.board_data[self.getpos(pos_y - 1)][self.getpos(pos_x)] != 0 or (
                    (self.checknext(pos_x)) and (self.board_data[self.getpos(pos_y - 1)][self.getpos(pos_x) + 1] != 0)):
                    return False

            if delta_y > 0:  # down
                if self.board_data[self.getpos(pos_y) + 1][self.getpos(pos_x)] != 0 or (
                    (self.checknext(pos_x)) and (self.board_data[self.getpos(pos_y) + 1][self.getpos(pos_x) + 1] != 0)):
                    return False
        except:
            return False
        return True
