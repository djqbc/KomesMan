from enum import IntEnum
from random import randint
import pygame

class MapTileType(IntEnum):
    '''Enum representing tile type'''
    NONE = 0
    RIGHT = 1
    LEFT = 2
    UP = 4
    DOWN = 8
    RIGHT_DOWN = RIGHT | DOWN
    RIGHT_UP = RIGHT | UP
    LEFT_UP = LEFT | UP
    LEFT_DOWN = LEFT | DOWN
    UP_DOWN = UP | DOWN
    LEFT_RIGHT = LEFT | RIGHT
    ALL = RIGHT | LEFT | UP | DOWN

class Map:
    map = [[]]
    size = 5;
    def __init__(self):
        pass
    def rule(self, _x, _y):
        fullSet = [e.value for e in MapTileType if e != MapTileType.NONE and e != MapTileType.ALL]
        
        if _x != 0:
#             if not self.map[_x - 1][_y] & MapTileType.DOWN:
#                 fullSet = [x for x in fullSet if not x & MapTileType.UP]
            pass
        else:
            fullSet = [x for x in fullSet if not x & MapTileType.UP]
        if _x + 1 != self.size:
#             if not self.map[_x + 1][_y] & MapTileType.UP:
#                 fullSet = [x for x in fullSet if not x & MapTileType.DOWN]
            pass
        else:
            fullSet = [x for x in fullSet if not x & MapTileType.DOWN]
        if _y != 0:
#             if not _left & MapTileType.RIGHT:
#                 fullSet = [x for x in fullSet if not x & MapTileType.LEFT]
            pass
        else:
            fullSet = [x for x in fullSet if not x & MapTileType.LEFT]
        if _y + 1 != self.size:
#             if not _right & MapTileType.LEFT:
#                 fullSet = [x for x in fullSet if not x & MapTileType.RIGHT]
            pass
        else:
            fullSet = [x for x in fullSet if not x & MapTileType.RIGHT]
        return fullSet
        
    def generate(self):
        size = 5
        self.map = [[MapTileType.NONE for x in range(size)] for y in range(size)] 
        for x in range(size):
            for y in range(size):
                available = self.rule(x, y)
                self.map[x][y] = available[randint(0, len(available) - 1)]
                
    def draw(self, _screen):
        tiles = {
            MapTileType.RIGHT_DOWN : pygame.image.load('res/img/wall001.png'),
            MapTileType.RIGHT_UP : pygame.image.load('res/img/wall002.png'),
            MapTileType.LEFT_UP : pygame.image.load('res/img/wall003.png'),
            MapTileType.LEFT_DOWN : pygame.image.load('res/img/wall004.png'),
            MapTileType.UP_DOWN : pygame.image.load('res/img/wall005.png'),
            MapTileType.LEFT_RIGHT : pygame.image.load('res/img/wall006.png'),
            MapTileType.LEFT : pygame.image.load('res/img/wall007.png'),
            MapTileType.UP : pygame.image.load('res/img/wall008.png'),
            MapTileType.RIGHT : pygame.image.load('res/img/wall009.png'),
            MapTileType.DOWN : pygame.image.load('res/img/wall010.png'),
            MapTileType.NONE : pygame.image.load('res/img/wall011.png')
            }                
        for x in range(5):
            for y in range(5):
                _screen.blit(tiles[self.map[x][y]], (y * 64, x * 64))