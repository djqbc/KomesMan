from sprite.mysprite import MySprite
import pygame


class DummySprite(MySprite):
    """Dummy sprite"""

    def __init__(self, tilesize):
        super(DummySprite, self).__init__()
        self.rect = pygame.Rect(0, 0, tilesize, tilesize)

    def draw(self, _screen, _positionx, _positiony):
        pass

    def update(self, _delta):
        MySprite.update(self, _delta)
