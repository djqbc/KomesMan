from enum import Enum
import pygame
from sprite.mysprite import MySprite

class WallKind(Enum):
    '''Enum representing animation state'''
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


class WallSprite(MySprite):
    '''Sprite of wall'''
    wallkinds = {
        WallKind.CORNER_TOPLEFT : 'res/img/wall001.png',
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
    }

    def __init__(self, wallkind):
        super(WallSprite, self).__init__()
        self.image = pygame.image.load(self.wallkinds[wallkind]);

    def draw(self, _screen, _positionX, _positionY):
        _screen.blit(self.image, (_positionX, _positionY))

    def update(self, _delta):
        MySprite.update(self, _delta)