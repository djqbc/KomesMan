from enum import Enum
import pygame
from sprite.mysprite import MySprite


class WallKind(Enum):
    """Enum representing animation state"""
    NONE = 0
    CORNER_TOPLEFT = 1
    CORNER_BOTTOMLEFT = 2
    CORNER_BOTTOMRIGHT = 3
    CORNER_TOPRIGHT = 4
    VERTICAL_WALL = 5
    HORIZONTAL_WALL = 6
    END_RIGHT = 7
    END_BOTTOM = 8
    END_LEFT = 9
    END_TOP = 10
    SQUARE = 11
    ONLY_TOP = 12
    ONLY_RIGHT = 13
    ONLY_BOTTOM = 14
    ONLY_LEFT = 15
    BLANK = 16


class WallKindDirection(Enum):
    IN = 0
    OUT = 1


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class WallKindTrueTable:
    table = {
        Direction.LEFT: {
            WallKindDirection.IN: [WallKind.CORNER_TOPLEFT, WallKind.CORNER_BOTTOMLEFT, WallKind.HORIZONTAL_WALL,
                                   WallKind.END_LEFT, WallKind.NONE],
            WallKindDirection.OUT: [WallKind.CORNER_BOTTOMRIGHT, WallKind.CORNER_TOPRIGHT, WallKind.HORIZONTAL_WALL,
                                    WallKind.END_RIGHT, WallKind.NONE]
        },
        Direction.RIGHT: {
            WallKindDirection.IN: [WallKind.CORNER_BOTTOMRIGHT, WallKind.CORNER_TOPRIGHT, WallKind.HORIZONTAL_WALL,
                                   WallKind.END_RIGHT, WallKind.NONE],
            WallKindDirection.OUT: [WallKind.CORNER_TOPLEFT, WallKind.CORNER_BOTTOMLEFT, WallKind.HORIZONTAL_WALL,
                                    WallKind.END_LEFT, WallKind.NONE]
        },
        Direction.UP: {
            WallKindDirection.IN: [WallKind.CORNER_TOPLEFT, WallKind.CORNER_TOPRIGHT, WallKind.VERTICAL_WALL,
                                   WallKind.END_TOP, WallKind.NONE],
            WallKindDirection.OUT: [WallKind.CORNER_BOTTOMLEFT, WallKind.CORNER_BOTTOMRIGHT, WallKind.VERTICAL_WALL,
                                    WallKind.END_BOTTOM, WallKind.NONE]
        },
        Direction.DOWN: {
            WallKindDirection.IN: [WallKind.CORNER_BOTTOMLEFT, WallKind.CORNER_BOTTOMRIGHT, WallKind.VERTICAL_WALL,
                                   WallKind.END_BOTTOM, WallKind.NONE],
            WallKindDirection.OUT: [WallKind.CORNER_TOPLEFT, WallKind.CORNER_TOPRIGHT, WallKind.VERTICAL_WALL,
                                    WallKind.END_TOP, WallKind.NONE]
        }
    }


class WallSprite(MySprite):
    """Sprite of wall"""
    wallkinds = {
        WallKind.CORNER_TOPLEFT: 'res/img/wall001.png',
        WallKind.CORNER_BOTTOMLEFT: 'res/img/wall002.png',
        WallKind.CORNER_BOTTOMRIGHT: 'res/img/wall003.png',
        WallKind.CORNER_TOPRIGHT: 'res/img/wall004.png',
        WallKind.VERTICAL_WALL: 'res/img/wall005.png',
        WallKind.HORIZONTAL_WALL: 'res/img/wall006.png',
        WallKind.END_RIGHT: 'res/img/wall007.png',
        WallKind.END_BOTTOM: 'res/img/wall008.png',
        WallKind.END_LEFT: 'res/img/wall009.png',
        WallKind.END_TOP: 'res/img/wall010.png',
        WallKind.SQUARE: 'res/img/wall011.png',
        WallKind.ONLY_TOP: 'res/img/wall012.png',
        WallKind.ONLY_RIGHT: 'res/img/wall013.png',
        WallKind.ONLY_BOTTOM: 'res/img/wall014.png',
        WallKind.ONLY_LEFT: 'res/img/wall015.png',
        WallKind.BLANK: 'res/img/wall016.png'
    }

    def __init__(self, wallkind, tilesize):
        super(WallSprite, self).__init__()
        self.wallkind = wallkind
        self.image = pygame.image.load(self.wallkinds[wallkind])
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))

    def draw(self, _screen, _positionx, _positiony):
        """
        Draws wall item, depending on set wall kind.
        :param _screen: screen surface
        :param _positionx: X position to draw item
        :param _positiony: Y position to draw item
        :return: nothing
        """
        _screen.blit(self.image, (_positionx, _positiony))

    def update(self, _delta):
        MySprite.update(self, _delta)
