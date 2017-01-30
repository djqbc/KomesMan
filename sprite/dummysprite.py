"""
Dummy sprite package
"""
from sprite.mysprite import MySprite
import pygame


class DummySprite(MySprite):
    """Dummy sprite"""

    def __init__(self, tilesize):
        """
        Constructor.
        :param tilesize: desired width and height of tile in pixels.
        """
        super(DummySprite, self).__init__()
        self.rect = pygame.Rect(0, 0, tilesize, tilesize)

    def draw(self, _screen, _positionx, _positiony):
        """
        Dummy sprite item
        :param _screen: unused
        :param _positionx: unused
        :param _positiony: unused
        :return: nothing
        """
        pass

    def update(self, _delta):
        """
        Update sprite
        :param _delta:
        :return: nothing
        """
        MySprite.update(self, _delta)
