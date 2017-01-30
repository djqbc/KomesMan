"""Drug sprite package."""
from sprite.mysprite import MySprite
import pygame


class DrugSprite(MySprite):
    """Sprite for Drug item - one inhalation and everything is better ;)."""

    def __init__(self, tilesize):
        """
        Constructor.

        :param tilesize: desired width and height of tile in pixels.
        """
        super(DrugSprite, self).__init__()
        self.image = pygame.image.load('res/img/powderbag.png')
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect()

    def draw(self, _screen, _positionx, _positiony):
        """
        Draw item.

        :param _screen: screen surface
        :param _positionx: X position to draw item
        :param _positiony: Y position to draw item
        :return: nothing
        """
        _screen.blit(self.image, (_positionx, _positiony))

    def update(self, _delta):
        """
        Update sprite.

        :param _delta:
        :return: nothing
        """
        MySprite.update(self, _delta)
