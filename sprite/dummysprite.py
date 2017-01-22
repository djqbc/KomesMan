from sprite.mysprite import MySprite
import pygame

class DummySprite(MySprite):
    """Dummy sprite"""
    def __init__(self):
        super(DummySprite, self).__init__()
        self.rect = pygame.Rect(0, 0, 64, 64)
    def draw(self, _screen, _positionX, _positionY):
        pass
    def update(self, _delta):
        MySprite.update(self, _delta)