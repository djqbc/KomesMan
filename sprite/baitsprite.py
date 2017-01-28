from sprite.mysprite import MySprite
import pygame


class BaitSprite(MySprite):
    """Bait item"""

    def __init__(self, tilesize):
        super(BaitSprite, self).__init__()
        self.image = pygame.image.load('res/img/bait.png')
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
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
        MySprite.update(self, _delta)
