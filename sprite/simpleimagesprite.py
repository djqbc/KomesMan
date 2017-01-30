"""
Simple image sprite package
"""
from sprite.mysprite import MySprite
import pygame


class SimpleImageSprite(MySprite):
    """SimpleImageSprite"""

    def __init__(self, _path):
        """
        Constructor
        :param _path: Path to image
        """
        super(SimpleImageSprite, self).__init__()
        self.image = pygame.image.load(_path)
        self.rect = self.image.get_rect()

    def draw(self, _screen, _positionx, _positiony):
        """
        Draw item
        :param _screen: screen surface
        :param _positionx: X position to draw item
        :param _positiony: Y position to draw item
        :return: nothing
        """
        _screen.blit(self.image, (_positionx, _positiony))

    def update(self, _delta):
        """
        Update sprite
        :param _delta:
        :return: nothing
        """
        MySprite.update(self, _delta)

    def size(self):
        """
        Get size of image
        :return: size of image
        """
        return self.image.get_size()

    def scale(self, xdim, ydim):
        """
        Scale image.
        :param xdim: X dimension in pixels
        :param ydim: Y dimension in pixels
        :return: nothing
        """
        self.image = pygame.transform.scale(self.image, (xdim, ydim))
