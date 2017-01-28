from sprite.mysprite import MySprite
import pygame


class TestSprite(MySprite):
    """
    Fake class used for testing purposes
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill((255, 0, 0))

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
